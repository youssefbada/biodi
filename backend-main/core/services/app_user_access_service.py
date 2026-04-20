import logging
from django.utils import timezone

from core.constants.error_codes import ErrorCodes
from core.exceptions.api_exceptions import (
    NotFoundApiException,
    ConflictApiException,
)
from core.models import AppUser

logger = logging.getLogger(__name__)


def get_active_app_user_by_nni(nni: str) -> AppUser:
    normalized_nni = (nni or "").strip()

    logger.info("Fetching app user by nni | nni=%s", normalized_nni)

    if not normalized_nni:
        logger.warning("Missing nni for app user lookup")
        raise NotFoundApiException(code=ErrorCodes.APP_USER_NOT_FOUND)

    try:
        app_user = AppUser.objects.get(nni=normalized_nni)
    except AppUser.DoesNotExist:
        logger.warning("App user not found | nni=%s", normalized_nni)
        raise NotFoundApiException(code=ErrorCodes.APP_USER_NOT_FOUND)

    if not app_user.is_active:
        logger.warning("Inactive app user | id=%s | nni=%s", app_user.id, normalized_nni)
        raise ConflictApiException(code=ErrorCodes.APP_USER_INACTIVE)

    return app_user


def mark_app_user_login(app_user: AppUser) -> AppUser:
    logger.info("Updating last login | app_user_id=%s | nni=%s", app_user.id, app_user.nni)

    app_user.last_login_at = timezone.now()
    app_user.save(update_fields=["last_login_at", "updated_at"])

    return app_user
