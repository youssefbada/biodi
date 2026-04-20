import logging
from django.db import transaction
from django.db.models import QuerySet

from core.constants.error_codes import ErrorCodes
from core.converters.inventaire_milieu_converter import (
  inventaire_milieu_model_to_dto,
  inventaire_milieu_upsert_dto_to_fields,
)
from core.dto.inventaire_milieu_dto import (
  InventaireMilieuDTO,
  InventaireMilieuUpsertDTO,
)
from core.exceptions.api_exceptions import (
  NotFoundApiException,
  ConflictApiException,
)
from core.models import InventaireMilieu, Centrales, Poissons, NonPoissons

logger = logging.getLogger(__name__)


def _validate_fk_ids(dto: InventaireMilieuUpsertDTO):
  if dto.centrale_id is None:
    raise ConflictApiException(code=ErrorCodes.INVENTAIRE_INVALID_RELATIONS)

  if not Centrales.objects.filter(pk=dto.centrale_id).exists():
    raise NotFoundApiException(code=ErrorCodes.CENTRALE_NOT_FOUND)

  if dto.espece_poisson_id is not None and dto.espece_non_poisson_id is not None:
    raise ConflictApiException(code=ErrorCodes.INVENTAIRE_INVALID_RELATIONS)

  if dto.espece_poisson_id is None and dto.espece_non_poisson_id is None:
    raise ConflictApiException(code=ErrorCodes.INVENTAIRE_INVALID_RELATIONS)

  if dto.espece_poisson_id is not None and not Poissons.objects.filter(pk=dto.espece_poisson_id).exists():
    raise NotFoundApiException(code=ErrorCodes.POISSON_NOT_FOUND)

  if dto.espece_non_poisson_id is not None and not NonPoissons.objects.filter(pk=dto.espece_non_poisson_id).exists():
    raise NotFoundApiException(code=ErrorCodes.NON_POISSON_NOT_FOUND)


def _validate_fk_fields_for_partial(fields: dict):
  centrale_id = fields.get("centrale_id")
  espece_poisson_id = fields.get("espece_poisson_id")
  espece_non_poisson_id = fields.get("espece_non_poisson_id")

  if centrale_id is not None and not Centrales.objects.filter(pk=centrale_id).exists():
    raise NotFoundApiException(code=ErrorCodes.CENTRALE_NOT_FOUND)

  if espece_poisson_id is not None and not Poissons.objects.filter(pk=espece_poisson_id).exists():
    raise NotFoundApiException(code=ErrorCodes.POISSON_NOT_FOUND)

  if espece_non_poisson_id is not None and not NonPoissons.objects.filter(pk=espece_non_poisson_id).exists():
    raise NotFoundApiException(code=ErrorCodes.NON_POISSON_NOT_FOUND)


def _inventaire_exists(
  centrale_id: int,
  espece_poisson_id: int | None,
  espece_non_poisson_id: int | None,
  exclude_id: int | None = None,
) -> bool:
  qs = InventaireMilieu.objects.filter(
    centrale_id=centrale_id,
    espece_poisson_id=espece_poisson_id,
    espece_non_poisson_id=espece_non_poisson_id,
  )

  if exclude_id is not None:
    qs = qs.exclude(pk=exclude_id)

  return qs.exists()


def list_inventaires_milieu() -> list[InventaireMilieuDTO]:
  logger.info("Listing inventaires milieu")

  qs: QuerySet[InventaireMilieu] = (
    InventaireMilieu.objects
    .select_related("centrale", "espece_poisson", "espece_non_poisson")
    .all()
    .order_by("-id_inventaire")
  )

  dtos = [inventaire_milieu_model_to_dto(obj) for obj in qs]
  logger.info("Listed inventaires milieu | count=%s", len(dtos))
  return dtos


def get_inventaire_milieu(inventaire_id: int) -> InventaireMilieuDTO:
  logger.info("Fetching inventaire milieu | id=%s", inventaire_id)

  try:
    obj = (
      InventaireMilieu.objects
      .select_related("centrale", "espece_poisson", "espece_non_poisson")
      .get(pk=inventaire_id)
    )
  except InventaireMilieu.DoesNotExist:
    logger.warning("Inventaire milieu not found | id=%s", inventaire_id)
    raise NotFoundApiException(code=ErrorCodes.INVENTAIRE_NOT_FOUND)

  return inventaire_milieu_model_to_dto(obj)


@transaction.atomic
def create_inventaire_milieu(dto: InventaireMilieuUpsertDTO) -> InventaireMilieuDTO:
  logger.info(
    "Creating inventaire milieu | centrale_id=%s | espece_poisson_id=%s | espece_non_poisson_id=%s",
    dto.centrale_id,
    dto.espece_poisson_id,
    dto.espece_non_poisson_id,
  )

  _validate_fk_ids(dto)

  if _inventaire_exists(
    centrale_id=dto.centrale_id,
    espece_poisson_id=dto.espece_poisson_id,
    espece_non_poisson_id=dto.espece_non_poisson_id,
  ):
    logger.warning(
      "Inventaire milieu already exists | centrale_id=%s | espece_poisson_id=%s | espece_non_poisson_id=%s",
      dto.centrale_id,
      dto.espece_poisson_id,
      dto.espece_non_poisson_id,
    )
    raise ConflictApiException(code=ErrorCodes.INVENTAIRE_ALREADY_EXISTS)

  fields = inventaire_milieu_upsert_dto_to_fields(dto)

  obj = InventaireMilieu.objects.create(**fields)

  logger.info("Inventaire milieu created | id=%s", obj.id_inventaire)

  obj = (
    InventaireMilieu.objects
    .select_related("centrale", "espece_poisson", "espece_non_poisson")
    .get(pk=obj.pk)
  )
  return inventaire_milieu_model_to_dto(obj)


@transaction.atomic
def update_inventaire_milieu(
  inventaire_id: int,
  dto: InventaireMilieuUpsertDTO,
) -> InventaireMilieuDTO:
  logger.info("Updating inventaire milieu | id=%s", inventaire_id)

  try:
    obj = InventaireMilieu.objects.get(pk=inventaire_id)
  except InventaireMilieu.DoesNotExist:
    logger.warning("Inventaire milieu not found for update | id=%s", inventaire_id)
    raise NotFoundApiException(code=ErrorCodes.INVENTAIRE_NOT_FOUND)

  _validate_fk_ids(dto)

  if _inventaire_exists(
    centrale_id=dto.centrale_id,
    espece_poisson_id=dto.espece_poisson_id,
    espece_non_poisson_id=dto.espece_non_poisson_id,
    exclude_id=inventaire_id,
  ):
    logger.warning(
      "Inventaire milieu duplicate on update | id=%s | centrale_id=%s | espece_poisson_id=%s | espece_non_poisson_id=%s",
      inventaire_id,
      dto.centrale_id,
      dto.espece_poisson_id,
      dto.espece_non_poisson_id,
    )
    raise ConflictApiException(code=ErrorCodes.INVENTAIRE_ALREADY_EXISTS)

  fields = inventaire_milieu_upsert_dto_to_fields(dto)

  for key, value in fields.items():
    setattr(obj, key, value)

  obj.full_clean()
  obj.save()

  logger.info("Inventaire milieu updated | id=%s", inventaire_id)

  obj = (
    InventaireMilieu.objects
    .select_related("centrale", "espece_poisson", "espece_non_poisson")
    .get(pk=obj.pk)
  )
  return inventaire_milieu_model_to_dto(obj)


@transaction.atomic
def partial_update_inventaire_milieu(
  inventaire_id: int,
  fields: dict,
) -> InventaireMilieuDTO:
  logger.info(
    "Partial updating inventaire milieu | id=%s | fields=%s",
    inventaire_id,
    list(fields.keys()),
  )

  try:
    obj = InventaireMilieu.objects.get(pk=inventaire_id)
  except InventaireMilieu.DoesNotExist:
    logger.warning("Inventaire milieu not found for partial update | id=%s", inventaire_id)
    raise NotFoundApiException(code=ErrorCodes.INVENTAIRE_NOT_FOUND)

  _validate_fk_fields_for_partial(fields)

  new_centrale_id = fields.get("centrale_id", obj.centrale_id)
  new_espece_poisson_id = fields.get("espece_poisson_id", obj.espece_poisson_id)
  new_espece_non_poisson_id = fields.get("espece_non_poisson_id", obj.espece_non_poisson_id)

  if new_centrale_id is None:
    raise ConflictApiException(code=ErrorCodes.INVENTAIRE_INVALID_RELATIONS)

  if new_espece_poisson_id is not None and new_espece_non_poisson_id is not None:
    raise ConflictApiException(code=ErrorCodes.INVENTAIRE_INVALID_RELATIONS)

  if new_espece_poisson_id is None and new_espece_non_poisson_id is None:
    raise ConflictApiException(code=ErrorCodes.INVENTAIRE_INVALID_RELATIONS)

  if _inventaire_exists(
    centrale_id=new_centrale_id,
    espece_poisson_id=new_espece_poisson_id,
    espece_non_poisson_id=new_espece_non_poisson_id,
    exclude_id=inventaire_id,
  ):
    logger.warning(
      "Inventaire milieu duplicate on partial update | id=%s | centrale_id=%s | espece_poisson_id=%s | espece_non_poisson_id=%s",
      inventaire_id,
      new_centrale_id,
      new_espece_poisson_id,
      new_espece_non_poisson_id,
    )
    raise ConflictApiException(code=ErrorCodes.INVENTAIRE_ALREADY_EXISTS)

  for key, value in fields.items():
    setattr(obj, key, value)

  obj.full_clean()
  obj.save()

  logger.info("Inventaire milieu partially updated | id=%s", inventaire_id)

  obj = (
    InventaireMilieu.objects
    .select_related("centrale", "espece_poisson", "espece_non_poisson")
    .get(pk=obj.pk)
  )
  return inventaire_milieu_model_to_dto(obj)


@transaction.atomic
def delete_inventaire_milieu(inventaire_id: int) -> None:
  logger.info("Deleting inventaire milieu | id=%s", inventaire_id)

  try:
    obj = InventaireMilieu.objects.get(pk=inventaire_id)
  except InventaireMilieu.DoesNotExist:
    logger.warning("Inventaire milieu not found for delete | id=%s", inventaire_id)
    raise NotFoundApiException(code=ErrorCodes.INVENTAIRE_NOT_FOUND)

  obj.delete()
  logger.info("Inventaire milieu deleted | id=%s", inventaire_id)