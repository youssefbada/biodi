import logging

from django.db import transaction
from django.db.models import QuerySet

from core.constants.error_codes import ErrorCodes
from core.converters.centrales_converter import centrale_model_to_dto, centrale_upsert_dto_to_fields
from core.dto.centrales_dto import CentraleDTO, CentraleUpsertDTO
from core.exceptions.api_exceptions import (
  NotFoundApiException,
  ConflictApiException,
)
from core.models import Centrales

logger = logging.getLogger(__name__)


def list_centrales() -> list[CentraleDTO]:
  logger.info("Listing centrales...")

  qs: QuerySet[Centrales] = Centrales.objects.all().order_by("code_nom", "site_name")

  dtos = [centrale_model_to_dto(obj) for obj in qs]
  logger.info("Listed centrales | count=%s", len(dtos))
  return dtos


def get_centrale(centrale_id: int) -> CentraleDTO:
  logger.info("Fetching centrale | id=%s", centrale_id)

  try:
    obj = Centrales.objects.get(pk=centrale_id)
  except Centrales.DoesNotExist:
    logger.warning("Centrale not found | id=%s", centrale_id)
    raise NotFoundApiException(
      code=ErrorCodes.CENTRALE_NOT_FOUND,
    )

  return centrale_model_to_dto(obj)


@transaction.atomic
def create_centrale(dto: CentraleUpsertDTO) -> CentraleDTO:
  logger.info("Creating centrale | code_nom=%s | site_name=%s", dto.code_nom, dto.site_name)

  if dto.code_nom and Centrales.objects.filter(code_nom__iexact=dto.code_nom).exists():
    logger.warning("Centrale already exists | code_nom=%s", dto.code_nom)
    raise ConflictApiException(
      code=ErrorCodes.CENTRALE_ALREADY_EXISTS,
    )

  fields = centrale_upsert_dto_to_fields(dto)
  obj = Centrales.objects.create(**fields)

  logger.info("Centrale created | id=%s | code_nom=%s", obj.id, obj.code_nom)
  return centrale_model_to_dto(obj)


@transaction.atomic
def update_centrale(centrale_id: int, dto: CentraleUpsertDTO) -> CentraleDTO:
  logger.info("Updating centrale | id=%s | code_nom=%s", centrale_id, dto.code_nom)

  try:
    obj = Centrales.objects.get(pk=centrale_id)
  except Centrales.DoesNotExist:
    logger.warning("Centrale not found for update | id=%s", centrale_id)
    raise NotFoundApiException(
      code=ErrorCodes.CENTRALE_NOT_FOUND,
    )

  if dto.code_nom and Centrales.objects.filter(code_nom__iexact=dto.code_nom).exclude(pk=centrale_id).exists():
    logger.warning("Centrale duplicate code_nom on update | id=%s | code_nom=%s", centrale_id, dto.code_nom)
    raise ConflictApiException(
      code=ErrorCodes.CENTRALE_ALREADY_EXISTS,
    )

  fields = centrale_upsert_dto_to_fields(dto)
  for k, v in fields.items():
    setattr(obj, k, v)

  obj.full_clean()
  obj.save()

  logger.info("Centrale updated | id=%s", centrale_id)
  return centrale_model_to_dto(obj)


@transaction.atomic
def partial_update_centrale(centrale_id: int, fields: dict) -> CentraleDTO:
  logger.info("Partial updating centrale | id=%s | fields=%s", centrale_id, list(fields.keys()))

  try:
    obj = Centrales.objects.get(pk=centrale_id)
  except Centrales.DoesNotExist:
    logger.warning("Centrale not found for partial update | id=%s", centrale_id)
    raise NotFoundApiException(
      code=ErrorCodes.CENTRALE_NOT_FOUND,
    )

  code_nom = fields.get("code_nom")
  if code_nom and Centrales.objects.filter(code_nom__iexact=code_nom).exclude(pk=centrale_id).exists():
    logger.warning("Centrale duplicate code_nom on partial update | id=%s | code_nom=%s", centrale_id, code_nom)
    raise ConflictApiException(
      code=ErrorCodes.CENTRALE_ALREADY_EXISTS,
    )

  for k, v in fields.items():
    setattr(obj, k, v)

  obj.full_clean()
  obj.save()

  logger.info("Centrale partially updated | id=%s", centrale_id)
  return centrale_model_to_dto(obj)


@transaction.atomic
def delete_centrale(centrale_id: int) -> None:
  logger.info("Deleting centrale | id=%s", centrale_id)

  try:
    obj = Centrales.objects.get(pk=centrale_id)
  except Centrales.DoesNotExist:
    logger.warning("Centrale not found for delete | id=%s", centrale_id)
    raise NotFoundApiException(
      code=ErrorCodes.CENTRALE_NOT_FOUND,
    )

  obj.delete()
  logger.info("Centrale deleted | id=%s", centrale_id)
