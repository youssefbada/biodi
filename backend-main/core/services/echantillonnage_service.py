import logging
from django.db import transaction
from django.db.models import QuerySet

from core.constants.error_codes import ErrorCodes
from core.converters.echantillonnage_converter import (
  echantillonnage_model_to_dto,
  echantillonnage_upsert_dto_to_fields,
)
from core.dto.echantillonnage_dto import EchantillonnageDTO, EchantillonnageUpsertDTO
from core.exceptions.api_exceptions import NotFoundApiException, ConflictApiException
from core.models import Echantillonnage, Centrales, Poissons, NonPoissons

logger = logging.getLogger(__name__)


def _validate_fk_ids(dto: EchantillonnageUpsertDTO):
  if dto.centrale_id is None:
    raise ConflictApiException(code=ErrorCodes.ECHANTILLONNAGE_INVALID_RELATIONS)

  if not Centrales.objects.filter(pk=dto.centrale_id).exists():
    raise NotFoundApiException(code=ErrorCodes.CENTRALE_NOT_FOUND)

  if dto.poisson_id is not None and dto.non_poisson_id is not None:
    raise ConflictApiException(code=ErrorCodes.ECHANTILLONNAGE_INVALID_RELATIONS)

  if dto.poisson_id is None and dto.non_poisson_id is None:
    raise ConflictApiException(code=ErrorCodes.ECHANTILLONNAGE_INVALID_RELATIONS)

  if dto.poisson_id is not None and not Poissons.objects.filter(pk=dto.poisson_id).exists():
    raise NotFoundApiException(code=ErrorCodes.POISSON_NOT_FOUND)

  if dto.non_poisson_id is not None and not NonPoissons.objects.filter(pk=dto.non_poisson_id).exists():
    raise NotFoundApiException(code=ErrorCodes.NON_POISSON_NOT_FOUND)


def _validate_fk_fields_for_partial(fields: dict):
  centrale_id = fields.get("centrale_id")
  poisson_id = fields.get("poisson_id")
  non_poisson_id = fields.get("non_poisson_id")

  if centrale_id is not None and not Centrales.objects.filter(pk=centrale_id).exists():
    raise NotFoundApiException(code=ErrorCodes.CENTRALE_NOT_FOUND)

  if poisson_id is not None and not Poissons.objects.filter(pk=poisson_id).exists():
    raise NotFoundApiException(code=ErrorCodes.POISSON_NOT_FOUND)

  if non_poisson_id is not None and not NonPoissons.objects.filter(pk=non_poisson_id).exists():
    raise NotFoundApiException(code=ErrorCodes.NON_POISSON_NOT_FOUND)


def list_echantillonnages() -> list[EchantillonnageDTO]:
  logger.info("Listing echantillonnages")

  qs: QuerySet[Echantillonnage] = (
    Echantillonnage.objects
    .select_related("centrale", "poisson", "non_poisson")
    .all()
    .order_by("-id_echantillonnage")
  )

  dtos = [echantillonnage_model_to_dto(obj) for obj in qs]
  logger.info("Listed echantillonnages | count=%s", len(dtos))
  return dtos


def get_echantillonnage(echantillonnage_id: int) -> EchantillonnageDTO:
  logger.info("Fetching echantillonnage | id=%s", echantillonnage_id)

  try:
    obj = Echantillonnage.objects.select_related("centrale", "poisson", "non_poisson").get(pk=echantillonnage_id)
  except Echantillonnage.DoesNotExist:
    logger.warning("Echantillonnage not found | id=%s", echantillonnage_id)
    raise NotFoundApiException(code=ErrorCodes.ECHANTILLONNAGE_NOT_FOUND)

  return echantillonnage_model_to_dto(obj)


@transaction.atomic
def create_echantillonnage(dto: EchantillonnageUpsertDTO) -> EchantillonnageDTO:
  logger.info(
    "Creating echantillonnage | centrale_id=%s | poisson_id=%s | non_poisson_id=%s",
    dto.centrale_id,
    dto.poisson_id,
    dto.non_poisson_id,
  )

  _validate_fk_ids(dto)

  fields = echantillonnage_upsert_dto_to_fields(dto)
  obj = Echantillonnage.objects.create(**fields)

  logger.info("Echantillonnage created | id=%s", obj.id_echantillonnage)
  obj = Echantillonnage.objects.select_related("centrale", "poisson", "non_poisson").get(pk=obj.pk)
  return echantillonnage_model_to_dto(obj)


@transaction.atomic
def update_echantillonnage(echantillonnage_id: int, dto: EchantillonnageUpsertDTO) -> EchantillonnageDTO:
  logger.info("Updating echantillonnage | id=%s", echantillonnage_id)

  try:
    obj = Echantillonnage.objects.get(pk=echantillonnage_id)
  except Echantillonnage.DoesNotExist:
    logger.warning("Echantillonnage not found for update | id=%s", echantillonnage_id)
    raise NotFoundApiException(code=ErrorCodes.ECHANTILLONNAGE_NOT_FOUND)

  _validate_fk_ids(dto)

  fields = echantillonnage_upsert_dto_to_fields(dto)
  for key, value in fields.items():
    setattr(obj, key, value)

  obj.full_clean()
  obj.save()

  logger.info("Echantillonnage updated | id=%s", echantillonnage_id)
  obj = Echantillonnage.objects.select_related("centrale", "poisson", "non_poisson").get(pk=obj.pk)
  return echantillonnage_model_to_dto(obj)


@transaction.atomic
def partial_update_echantillonnage(echantillonnage_id: int, fields: dict) -> EchantillonnageDTO:
  logger.info(
    "Partial updating echantillonnage | id=%s | fields=%s",
    echantillonnage_id,
    list(fields.keys()),
  )

  try:
    obj = Echantillonnage.objects.get(pk=echantillonnage_id)
  except Echantillonnage.DoesNotExist:
    logger.warning("Echantillonnage not found for partial update | id=%s", echantillonnage_id)
    raise NotFoundApiException(code=ErrorCodes.ECHANTILLONNAGE_NOT_FOUND)

  _validate_fk_fields_for_partial(fields)

  new_poisson_id = fields.get("poisson_id", obj.poisson_id)
  new_non_poisson_id = fields.get("non_poisson_id", obj.non_poisson_id)

  if new_poisson_id and new_non_poisson_id:
    raise ConflictApiException(code=ErrorCodes.ECHANTILLONNAGE_INVALID_RELATIONS)

  if not new_poisson_id and not new_non_poisson_id:
    raise ConflictApiException(code=ErrorCodes.ECHANTILLONNAGE_INVALID_RELATIONS)

  for key, value in fields.items():
    setattr(obj, key, value)

  obj.full_clean()
  obj.save()

  logger.info("Echantillonnage partially updated | id=%s", echantillonnage_id)
  obj = Echantillonnage.objects.select_related("centrale", "poisson", "non_poisson").get(pk=obj.pk)
  return echantillonnage_model_to_dto(obj)


@transaction.atomic
def delete_echantillonnage(echantillonnage_id: int) -> None:
  logger.info("Deleting echantillonnage | id=%s", echantillonnage_id)

  try:
    obj = Echantillonnage.objects.get(pk=echantillonnage_id)
  except Echantillonnage.DoesNotExist:
    logger.warning("Echantillonnage not found for delete | id=%s", echantillonnage_id)
    raise NotFoundApiException(code=ErrorCodes.ECHANTILLONNAGE_NOT_FOUND)

  obj.delete()
  logger.info("Echantillonnage deleted | id=%s", echantillonnage_id)