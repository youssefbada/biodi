import logging
from typing import Any, Dict, List, Tuple

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q

from core.constants.error_codes import ErrorCodes
from core.exceptions.api_exceptions import ConflictApiException
from core.constants.query_builder_registry import QUERY_BUILDER_MODELS, get_model_config

logger = logging.getLogger(__name__)


ALLOWED_OPERATORS = {
  "eq",
  "neq",
  "lt",
  "lte",
  "gt",
  "gte",
  "contains",
  "icontains",
  "startswith",
  "istartswith",
  "endswith",
  "iendswith",
  "in",
  "isnull",
}

ALLOWED_LOGICS = {"AND", "OR", "NOT"}


def _get_concrete_field_names(model) -> set[str]:
  field_names = set()
  for field in model._meta.get_fields():
    if getattr(field, "concrete", False) and not field.is_relation:
      field_names.add(field.name)
  return field_names


def _resolve_field_path(root_key: str, dotted_path: str) -> Tuple[str, object]:
  """
  Ex:
   root = "echantillonnages"
   dotted_path = "centrale.code_nom"
   -> ("centrale__code_nom", CharField)
  """
  if not dotted_path:
    raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_FIELD)

  parts = dotted_path.split(".")
  current_config = get_model_config(root_key)
  current_model = current_config.model
  orm_parts: List[str] = []

  for index, part in enumerate(parts):
    is_last = index == len(parts) - 1

    if not is_last:
      if part not in current_config.relations:
        raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_RELATION)

      relation = current_config.relations[part]
      orm_parts.append(relation.orm_name)

      current_config = get_model_config(relation.target_key)
      current_model = current_config.model
    else:
      concrete_fields = _get_concrete_field_names(current_model)
      if part not in concrete_fields:
        raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_FIELD)

      try:
        django_field = current_model._meta.get_field(part)
      except FieldDoesNotExist:
        raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_FIELD)

      orm_parts.append(part)
      return "__".join(orm_parts), django_field

  raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_FIELD)


def _build_lookup_expression(orm_path: str, operator: str) -> str:
  if operator == "eq":
    return orm_path
  if operator == "neq":
    return orm_path
  if operator == "lt":
    return f"{orm_path}__lt"
  if operator == "lte":
    return f"{orm_path}__lte"
  if operator == "gt":
    return f"{orm_path}__gt"
  if operator == "gte":
    return f"{orm_path}__gte"
  if operator == "contains":
    return f"{orm_path}__contains"
  if operator == "icontains":
    return f"{orm_path}__icontains"
  if operator == "startswith":
    return f"{orm_path}__startswith"
  if operator == "istartswith":
    return f"{orm_path}__istartswith"
  if operator == "endswith":
    return f"{orm_path}__endswith"
  if operator == "iendswith":
    return f"{orm_path}__iendswith"
  if operator == "in":
    return f"{orm_path}__in"
  if operator == "isnull":
    return f"{orm_path}__isnull"

  raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_OPERATOR)


def _build_simple_condition(root_key: str, condition: Dict[str, Any]) -> Q:
  field = condition.get("field")
  operator = condition.get("operator")
  value = condition.get("value")

  if not field or not operator:
    raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_FILTER)

  if operator not in ALLOWED_OPERATORS:
    raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_OPERATOR)

  orm_path, _django_field = _resolve_field_path(root_key, field)

  if operator == "neq":
    return ~Q(**{orm_path: value})

  if operator == "in":
    if not isinstance(value, list):
      raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_FILTER)
    return Q(**{_build_lookup_expression(orm_path, operator): value})

  if operator == "isnull":
    if not isinstance(value, bool):
      raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_FILTER)
    return Q(**{_build_lookup_expression(orm_path, operator): value})

  return Q(**{_build_lookup_expression(orm_path, operator): value})


def _build_q_recursive(root_key: str, node: Dict[str, Any]) -> Q:
  """
  node peut être :
  - condition simple :
   {"field": "centrale.code_nom", "operator": "eq", "value": "GRA"}

  - groupe logique :
   {
    "logic": "AND",
    "conditions": [
     {...},
     {...}
    ]
   }
  """
  if "logic" not in node:
    return _build_simple_condition(root_key, node)

  logic = node.get("logic")
  conditions = node.get("conditions", [])

  if logic not in ALLOWED_LOGICS:
    raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_LOGIC)

  if not isinstance(conditions, list) or not conditions:
    raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_FILTER)

  built_conditions = [_build_q_recursive(root_key, child) for child in conditions]

  if logic == "AND":
    q = built_conditions[0]
    for child_q in built_conditions[1:]:
      q &= child_q
    return q

  if logic == "OR":
    q = built_conditions[0]
    for child_q in built_conditions[1:]:
      q |= child_q
    return q

  if logic == "NOT":
    if len(built_conditions) != 1:
      raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_FILTER)
    return ~built_conditions[0]

  raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_LOGIC)


def _build_values_mapping(root_key: str, select_fields: List[str]) -> Dict[str, str]:
  """
  Ex:
   ["id_echantillonnage", "centrale.code_nom"]
   ->
   {
    "id_echantillonnage": "id_echantillonnage",
    "centrale__code_nom": "centrale.code_nom"
   }
  """
  mapping = {}

  for field in select_fields:
    orm_path, _ = _resolve_field_path(root_key, field)
    mapping[field] = orm_path

  return mapping


def _build_order_by(root_key: str, order_by_config: List[Dict[str, Any]]) -> List[str]:
  clauses = []

  for item in order_by_config:
    field = item.get("field")
    direction = str(item.get("direction", "asc")).lower()

    if direction not in {"asc", "desc"}:
      raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_ORDER_BY)

    orm_path, _ = _resolve_field_path(root_key, field)
    clauses.append(f"-{orm_path}" if direction == "desc" else orm_path)

  return clauses

def get_query_builder_metadata() -> Dict[str, Any]:
  metadata = {"roots": []}

  for model_key, config in QUERY_BUILDER_MODELS.items():
    model = config.model
    fields = []

    for field in model._meta.get_fields():
      if getattr(field, "concrete", False) and not field.is_relation:

        # Récupérer les choices si disponibles
        choices = None
        if hasattr(field, "choices") and field.choices:
          choices = [{"value": c[0], "label": c[1]} for c in field.choices]

        # Détecter BooleanField
        field_type = field.get_internal_type()

        fields.append(
          {
            "name": field.name,
            "label": getattr(field, "verbose_name", field.name),
            "type": field_type,
            "choices": choices,
          }
        )

    relations = []
    for alias, relation in config.relations.items():
      target = QUERY_BUILDER_MODELS[relation.target_key]
      relations.append(
        {
          "alias": alias,
          "target": relation.target_key,
          "target_label": target.label,
        }
      )

    metadata["roots"].append(
      {
        "key": model_key,
        "label": config.label,
        "fields": fields,
        "relations": relations,
      }
    )

  return metadata

# def get_query_builder_metadata() -> Dict[str, Any]:
#   metadata = {"roots": []}

#   for model_key, config in QUERY_BUILDER_MODELS.items():
#     model = config.model
#     fields = []

#     for field in model._meta.get_fields():
#       if getattr(field, "concrete", False) and not field.is_relation:
#         fields.append(
#           {
#             "name": field.name,
#             "label": getattr(field, "verbose_name", field.name),
#             "type": field.get_internal_type(),
#           }
#         )

#     relations = []
#     for alias, relation in config.relations.items():
#       target = QUERY_BUILDER_MODELS[relation.target_key]
#       relations.append(
#         {
#           "alias": alias,
#           "target": relation.target_key,
#           "target_label": target.label,
#         }
#       )

#     metadata["roots"].append(
#       {
#         "key": model_key,
#         "label": config.label,
#         "fields": fields,
#         "relations": relations,
#       }
#     )

#   return metadata


def execute_query_builder(payload: Dict[str, Any]) -> Dict[str, Any]:
  root = payload["root"]
  select_fields = payload["select"]
  filters = payload.get("filters")
  order_by_config = payload.get("order_by", [])
  distinct = payload.get("distinct", False)
  limit = payload.get("limit", 500)

  logger.info(
    "Executing query builder | root=%s | select_count=%s | distinct=%s | limit=%s",
    root,
    len(select_fields),
    distinct,
    limit,
  )

  if root not in QUERY_BUILDER_MODELS:
    raise ConflictApiException(code=ErrorCodes.QUERY_BUILDER_INVALID_ROOT)

  root_config = get_model_config(root)
  qs = root_config.model.objects.all()

  if filters:
    q_object = _build_q_recursive(root, filters)
    qs = qs.filter(q_object)

  if distinct:
    qs = qs.distinct()

  if order_by_config:
    order_by_clauses = _build_order_by(root, order_by_config)
    qs = qs.order_by(*order_by_clauses)

  select_mapping = _build_values_mapping(root, select_fields)

  values_qs = qs.values(*select_mapping.values())[:limit]

  rows = []
  for row in values_qs:
    formatted_row = {}
    for front_field, orm_field in select_mapping.items():
      formatted_row[front_field] = row.get(orm_field)
    rows.append(formatted_row)

  logger.info(
    "Query builder executed successfully | root=%s | row_count=%s",
    root,
    len(rows),
  )

  return {
    "root": root,
    "columns": select_fields,
    "rows": rows,
    "count": len(rows),
  }