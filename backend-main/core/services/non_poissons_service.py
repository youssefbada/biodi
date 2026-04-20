import logging
from django.db import transaction
from django.db.models import QuerySet

from core.constants.error_codes import ErrorCodes
from core.converters.non_poissons_converter import (
  non_poisson_model_to_dto,
  non_poisson_upsert_dto_to_fields,
)
from core.dto.non_poissons_dto import NonPoissonDTO, NonPoissonUpsertDTO
from core.exceptions.api_exceptions import (
  NotFoundApiException,
  ConflictApiException,
)
from core.models import NonPoissons

logger = logging.getLogger(__name__)


def list_non_poissons() -> list[NonPoissonDTO]:
  logger.info("Listing non poissons")

  qs: QuerySet[NonPoissons] = NonPoissons.objects.all().order_by(
    "groupe", "famille", "genre", "espece", "nom_commun"
  )

  dtos = [non_poisson_model_to_dto(obj) for obj in qs]
  logger.info("Listed non poissons | count=%s", len(dtos))
  return dtos


def get_non_poisson(non_poisson_id: int) -> NonPoissonDTO:
  logger.info("Fetching non poisson | id=%s", non_poisson_id)

  try:
    obj = NonPoissons.objects.get(pk=non_poisson_id)
  except NonPoissons.DoesNotExist:
    logger.warning("Non poisson not found | id=%s", non_poisson_id)
    raise NotFoundApiException(
      code=ErrorCodes.NON_POISSON_NOT_FOUND,
    )

  return non_poisson_model_to_dto(obj)


def _non_poisson_exists(famille: str, genre: str, espece: str, exclude_id: int | None = None) -> bool:
  qs = NonPoissons.objects.filter(
    famille__iexact=(famille or "").strip(),
    genre__iexact=(genre or "").strip(),
    espece__iexact=(espece or "").strip(),
  )

  if exclude_id is not None:
    qs = qs.exclude(pk=exclude_id)

  return qs.exists()


@transaction.atomic
def create_non_poisson(dto: NonPoissonUpsertDTO) -> NonPoissonDTO:
  logger.info(
    "Creating non poisson | groupe=%s | famille=%s | genre=%s | espece=%s",
    dto.groupe,
    dto.famille,
    dto.genre,
    dto.espece,
  )

  if dto.famille and dto.genre and dto.espece:
    if _non_poisson_exists(dto.famille, dto.genre, dto.espece):
      logger.warning(
        "Non poisson already exists | groupe=%s | famille=%s | genre=%s | espece=%s",
        dto.groupe,
        dto.famille,
        dto.genre,
        dto.espece,
      )
      raise ConflictApiException(
        code=ErrorCodes.NON_POISSON_ALREADY_EXISTS,
      )

  fields = non_poisson_upsert_dto_to_fields(dto)
  obj = NonPoissons.objects.create(**fields)

  logger.info("Non poisson created | id=%s", obj.id_non_poisson)
  return non_poisson_model_to_dto(obj)

@transaction.atomic
def update_non_poisson(non_poisson_id: int, dto: NonPoissonUpsertDTO) -> NonPoissonDTO:
  logger.info("Updating non poisson | id=%s", non_poisson_id)

  try:
    obj = NonPoissons.objects.get(pk=non_poisson_id)
  except NonPoissons.DoesNotExist:
    logger.warning("Non poisson not found for update | id=%s", non_poisson_id)
    raise NotFoundApiException(
      code=ErrorCodes.NON_POISSON_NOT_FOUND,
    )

  if dto.famille and dto.genre and dto.espece:
    if _non_poisson_exists(dto.famille, dto.genre, dto.espece, exclude_id=non_poisson_id):
      logger.warning(
        "Non poisson duplicate on update | id=%s | groupe=%s | famille=%s | genre=%s | espece=%s",
        non_poisson_id,
        dto.groupe,
        dto.famille,
        dto.genre,
        dto.espece,
      )
      raise ConflictApiException(
        code=ErrorCodes.NON_POISSON_ALREADY_EXISTS,
      )

  fields = non_poisson_upsert_dto_to_fields(dto)

  for key, value in fields.items():
    setattr(obj, key, value)

  obj.full_clean()
  obj.save()

  logger.info("Non poisson updated | id=%s", non_poisson_id)
  return non_poisson_model_to_dto(obj)


@transaction.atomic
def partial_update_non_poisson(non_poisson_id: int, fields: dict) -> NonPoissonDTO:
  logger.info(
    "Partial updating non poisson | id=%s | fields=%s",
    non_poisson_id,
    list(fields.keys()),
  )

  try:
    obj = NonPoissons.objects.get(pk=non_poisson_id)
  except NonPoissons.DoesNotExist:
    logger.warning("Non poisson not found for partial update | id=%s", non_poisson_id)
    raise NotFoundApiException(
      code=ErrorCodes.NON_POISSON_NOT_FOUND,
    )

  groupe = fields.get("groupe", obj.groupe)
  famille = fields.get("famille", obj.famille)
  genre = fields.get("genre", obj.genre)
  espece = fields.get("espece", obj.espece)

  if famille and genre and espece:
    if _non_poisson_exists(famille, genre, espece, exclude_id=non_poisson_id):
      logger.warning(
        "Non poisson duplicate on partial update | id=%s | groupe=%s | famille=%s | genre=%s | espece=%s",
        non_poisson_id,
        groupe,
        famille,
        genre,
        espece,
      )
      raise ConflictApiException(
        code=ErrorCodes.NON_POISSON_ALREADY_EXISTS,
      )

  for key, value in fields.items():
    setattr(obj, key, value)

  obj.full_clean()
  obj.save()

  logger.info("Non poisson partially updated | id=%s", non_poisson_id)
  return non_poisson_model_to_dto(obj)


@transaction.atomic
def delete_non_poisson(non_poisson_id: int) -> None:
  logger.info("Deleting non poisson | id=%s", non_poisson_id)

  try:
    obj = NonPoissons.objects.get(pk=non_poisson_id)
  except NonPoissons.DoesNotExist:
    logger.warning("Non poisson not found for delete | id=%s", non_poisson_id)
    raise NotFoundApiException(
      code=ErrorCodes.NON_POISSON_NOT_FOUND,
    )

  obj.delete()
  logger.info("Non poisson deleted | id=%s", non_poisson_id)