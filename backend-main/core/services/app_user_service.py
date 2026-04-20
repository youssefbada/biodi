import logging
from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from core.constants.error_codes import ErrorCodes
from core.converters.app_user_converter import (
    app_user_model_to_dto,
    app_user_upsert_dto_to_fields,
)
from core.dto.app_user_dto import AppUserDTO, AppUserUpsertDTO
from core.exceptions.api_exceptions import (
    NotFoundApiException,
    ConflictApiException,
)
from core.models import AppUser, AppUserRole

logger = logging.getLogger(__name__)


def _normalize_nni(value: str) -> str:
    return (value or "").strip()


def _normalize_email(value: str) -> str:
    return (value or "").strip().lower()


def _is_valid_role(role: str) -> bool:
    return role in {AppUserRole.ADMIN, AppUserRole.READ_ONLY}


def _app_user_exists(nni: str, email: str, exclude_id: int | None = None) -> bool:
    normalized_nni = _normalize_nni(nni)
    normalized_email = _normalize_email(email)

    qs = AppUser.objects.filter(nni__iexact=normalized_nni) | AppUser.objects.filter(email__iexact=normalized_email)

    if exclude_id is not None:
        qs = qs.exclude(pk=exclude_id)

    return qs.exists()


def list_app_users() -> list[AppUserDTO]:
    logger.info("Listing app users")

    qs: QuerySet[AppUser] = AppUser.objects.all().order_by("email")
    dtos = [app_user_model_to_dto(obj) for obj in qs]

    logger.info("Listed app users | count=%s", len(dtos))
    return dtos


def get_app_user(app_user_id: int) -> AppUserDTO:
    logger.info("Fetching app user | id=%s", app_user_id)

    try:
        obj = AppUser.objects.get(pk=app_user_id)
    except AppUser.DoesNotExist:
        logger.warning("App user not found | id=%s", app_user_id)
        raise NotFoundApiException(code=ErrorCodes.APP_USER_NOT_FOUND)

    return app_user_model_to_dto(obj)


def get_active_app_user_by_nni(nni: str) -> AppUser:
    normalized_nni = _normalize_nni(nni)
    logger.info("Fetching active app user by nni | nni=%s", normalized_nni)

    try:
        obj = AppUser.objects.get(nni=normalized_nni)
    except AppUser.DoesNotExist:
        logger.warning("App user not found by nni | nni=%s", normalized_nni)
        raise NotFoundApiException(code=ErrorCodes.APP_USER_NOT_FOUND)

    if not obj.is_active:
        logger.warning("Inactive app user | id=%s | nni=%s", obj.id, normalized_nni)
        raise ConflictApiException(code=ErrorCodes.APP_USER_INACTIVE)

    return obj


@transaction.atomic
def create_app_user(dto: AppUserUpsertDTO) -> AppUserDTO:
    normalized_nni = _normalize_nni(dto.nni)
    normalized_email = _normalize_email(dto.email)

    logger.info(
        "Creating app user | nni=%s | email=%s | role=%s",
        normalized_nni,
        normalized_email,
        dto.role,
    )

    if not _is_valid_role(dto.role):
        logger.warning("Invalid app user role on create | role=%s", dto.role)
        raise ConflictApiException(code=ErrorCodes.APP_USER_INVALID_ROLE)

    if _app_user_exists(normalized_nni, normalized_email):
        logger.warning("App user already exists | nni=%s | email=%s", normalized_nni, normalized_email)
        raise ConflictApiException(code=ErrorCodes.APP_USER_ALREADY_EXISTS)

    fields = app_user_upsert_dto_to_fields(dto)
    fields["nni"] = normalized_nni
    fields["email"] = normalized_email

    obj = AppUser.objects.create(**fields)

    logger.info("App user created | id=%s | nni=%s", obj.id, obj.nni)
    return app_user_model_to_dto(obj)

@transaction.atomic
def partial_update_app_user(app_user_id: int, fields: dict) -> AppUserDTO:
    logger.info("Partial updating app user | id=%s | fields=%s", app_user_id, list(fields.keys()))

    try:
        obj = AppUser.objects.get(pk=app_user_id)
    except AppUser.DoesNotExist:
        logger.warning("App user not found for partial update | id=%s", app_user_id)
        raise NotFoundApiException(code=ErrorCodes.APP_USER_NOT_FOUND)

    new_nni = _normalize_nni(fields.get("nni", obj.nni))
    new_email = _normalize_email(fields.get("email", obj.email))
    new_role = fields.get("role", obj.role)

    if not _is_valid_role(new_role):
        logger.warning("Invalid app user role on partial update | id=%s | role=%s", app_user_id, new_role)
        raise ConflictApiException(code=ErrorCodes.APP_USER_INVALID_ROLE)

    if _app_user_exists(new_nni, new_email, exclude_id=app_user_id):
        logger.warning(
            "App user duplicate on partial update | id=%s | nni=%s | email=%s",
            app_user_id,
            new_nni,
            new_email,
        )
        raise ConflictApiException(code=ErrorCodes.APP_USER_ALREADY_EXISTS)

    for key, value in fields.items():
        if key == "nni":
            value = _normalize_nni(value)
        elif key == "email":
            value = _normalize_email(value)
        setattr(obj, key, value)

    obj.full_clean()
    obj.save()

    logger.info("App user partially updated | id=%s", app_user_id)
    return app_user_model_to_dto(obj)


@transaction.atomic
def delete_app_user(app_user_id: int) -> None:
    logger.info("Deleting app user | id=%s", app_user_id)

    try:
        obj = AppUser.objects.get(pk=app_user_id)
    except AppUser.DoesNotExist:
        logger.warning("App user not found for delete | id=%s", app_user_id)
        raise NotFoundApiException(code=ErrorCodes.APP_USER_NOT_FOUND)

    obj.delete()
    logger.info("App user deleted | id=%s", app_user_id)


@transaction.atomic
def mark_app_user_login(app_user: AppUser) -> AppUser:
    logger.info("Marking app user login | id=%s | nni=%s", app_user.id, app_user.nni)

    app_user.last_login_at = timezone.now()
    app_user.save(update_fields=["last_login_at", "updated_at"])

    return app_user
