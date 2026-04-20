from core.dto.inventaire_milieu_dto import (
  InventaireMilieuDTO,
  InventaireMilieuUpsertDTO,
)
from core.models import InventaireMilieu


def _centrale_label(obj):
  if not obj:
    return None
  return f"{obj.code_nom or ''} - {obj.site_name or ''}".strip(" -")


def _poisson_label(obj):
  if not obj:
    return None

  sci = " ".join([x for x in [obj.genre, obj.espece] if x])
  return f"{obj.nom_commun or ''} ({sci})".strip()


def _non_poisson_label(obj):
  if not obj:
    return None

  sci = " ".join([x for x in [obj.genre, obj.espece] if x])
  return f"{obj.nom_commun or ''} ({sci})".strip()


def inventaire_milieu_model_to_dto(obj: InventaireMilieu) -> InventaireMilieuDTO:
  return InventaireMilieuDTO(
    id_inventaire=obj.id_inventaire,

    centrale_id=obj.centrale_id,
    centrale_label=_centrale_label(obj.centrale),

    espece_poisson_id=obj.espece_poisson_id,
    espece_poisson_label=_poisson_label(obj.espece_poisson),

    espece_non_poisson_id=obj.espece_non_poisson_id,
    espece_non_poisson_label=_non_poisson_label(obj.espece_non_poisson),

    nom_commun=obj.nom_commun,

    groupe_poisson=obj.groupe_poisson,
    groupe_non_poisson=obj.groupe_non_poisson,
  )


def inventaire_milieu_upsert_dto_to_fields(dto: InventaireMilieuUpsertDTO) -> dict:
  return {
    "centrale_id": dto.centrale_id,
    "espece_poisson_id": dto.espece_poisson_id,
    "espece_non_poisson_id": dto.espece_non_poisson_id,
    "nom_commun": dto.nom_commun,
    "groupe_poisson": dto.groupe_poisson,
    "groupe_non_poisson": dto.groupe_non_poisson,
  }