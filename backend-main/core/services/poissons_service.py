import logging
from django.db import transaction
from django.db.models import QuerySet

from core.constants.error_codes import ErrorCodes
from core.converters.poissons_converter import (
  poisson_model_to_dto,
  poisson_upsert_dto_to_fields,
)
from core.dto.poissons_dto import PoissonDTO, PoissonUpsertDTO
from core.exceptions.api_exceptions import (
  NotFoundApiException,
  ConflictApiException,
)
from core.models import Poissons

logger = logging.getLogger(__name__)


def list_poissons() -> list[PoissonDTO]:
  logger.info("Listing poissons")

  qs: QuerySet[Poissons] = Poissons.objects.all().order_by(
    "famille", "genre", "espece", "nom_commun"
  )

  dtos = [poisson_model_to_dto(obj) for obj in qs]

  logger.info("Listed poissons | count=%s", len(dtos))
  return dtos


def get_poisson(poisson_id: int) -> PoissonDTO:
  logger.info("Fetching poisson | id=%s", poisson_id)

  try:
    obj = Poissons.objects.get(pk=poisson_id)
  except Poissons.DoesNotExist:
    logger.warning("Poisson not found | id=%s", poisson_id)
    raise NotFoundApiException(
      code=ErrorCodes.POISSON_NOT_FOUND,
    )

  return poisson_model_to_dto(obj)


def _poisson_exists(famille: str, genre: str, espece: str, exclude_id: int | None = None) -> bool:
  qs = Poissons.objects.filter(
    famille__iexact=(famille or "").strip(),
    genre__iexact=(genre or "").strip(),
    espece__iexact=(espece or "").strip(),
  )

  if exclude_id is not None:
    qs = qs.exclude(pk=exclude_id)

  return qs.exists()


@transaction.atomic
def create_poisson(dto: PoissonUpsertDTO) -> PoissonDTO:
  logger.info(
    "Creating poisson | famille=%s | genre=%s | espece=%s",
    dto.famille,
    dto.genre,
    dto.espece,
  )

  if dto.famille and dto.genre and dto.espece:
    if _poisson_exists(dto.famille, dto.genre, dto.espece):
      logger.warning(
        "Poisson already exists | famille=%s | genre=%s | espece=%s",
        dto.famille,
        dto.genre,
        dto.espece,
      )
      raise ConflictApiException(
        code=ErrorCodes.POISSON_ALREADY_EXISTS,
      )

  fields = poisson_upsert_dto_to_fields(dto)
  obj = Poissons.objects.create(**fields)

  logger.info("Poisson created | id=%s", obj.id_poisson)
  return poisson_model_to_dto(obj)


@transaction.atomic
def update_poisson(poisson_id: int, dto: PoissonUpsertDTO) -> PoissonDTO:
  logger.info("Updating poisson | id=%s", poisson_id)

  try:
    obj = Poissons.objects.get(pk=poisson_id)
  except Poissons.DoesNotExist:
    logger.warning("Poisson not found for update | id=%s", poisson_id)
    raise NotFoundApiException(
      code=ErrorCodes.POISSON_NOT_FOUND,
    )

  if dto.famille and dto.genre and dto.espece:
    if _poisson_exists(dto.famille, dto.genre, dto.espece, exclude_id=poisson_id):
      logger.warning(
        "Poisson duplicate on update | id=%s | famille=%s | genre=%s | espece=%s",
        poisson_id,
        dto.famille,
        dto.genre,
        dto.espece,
      )
      raise ConflictApiException(
        code=ErrorCodes.POISSON_ALREADY_EXISTS,
      )

  fields = poisson_upsert_dto_to_fields(dto)

  for key, value in fields.items():
    setattr(obj, key, value)

  obj.full_clean()
  obj.save()

  logger.info("Poisson updated | id=%s", poisson_id)
  return poisson_model_to_dto(obj)


@transaction.atomic
def partial_update_poisson(poisson_id: int, fields: dict) -> PoissonDTO:
  logger.info(
    "Partial updating poisson | id=%s | fields=%s",
    poisson_id,
    list(fields.keys()),
  )

  try:
    obj = Poissons.objects.get(pk=poisson_id)
  except Poissons.DoesNotExist:
    logger.warning("Poisson not found for partial update | id=%s", poisson_id)
    raise NotFoundApiException(
      code=ErrorCodes.POISSON_NOT_FOUND,
    )

  famille = fields.get("famille", obj.famille)
  genre = fields.get("genre", obj.genre)
  espece = fields.get("espece", obj.espece)

  if famille and genre and espece:
    if _poisson_exists(famille, genre, espece, exclude_id=poisson_id):
      logger.warning(
        "Poisson duplicate on partial update | id=%s | famille=%s | genre=%s | espece=%s",
        poisson_id,
        famille,
        genre,
        espece,
      )
      raise ConflictApiException(
        code=ErrorCodes.POISSON_ALREADY_EXISTS,
      )

  for key, value in fields.items():
    setattr(obj, key, value)

  obj.full_clean()
  obj.save()

  logger.info("Poisson partially updated | id=%s", poisson_id)
  return poisson_model_to_dto(obj)


@transaction.atomic
def delete_poisson(poisson_id: int) -> None:
  logger.info("Deleting poisson | id=%s", poisson_id)

  try:
    obj = Poissons.objects.get(pk=poisson_id)
  except Poissons.DoesNotExist:
    logger.warning("Poisson not found for delete | id=%s", poisson_id)
    raise NotFoundApiException(
      code=ErrorCodes.POISSON_NOT_FOUND,
    )

  obj.delete()
  logger.info("Poisson deleted | id=%s", poisson_id)