import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError

from core.utils.api_utils import build_error_response
from core.constants.error_codes import ErrorCodes
from core.constants.error_messages import ERROR_MESSAGES
from core.exceptions.api_exceptions import ApiException

from core.serializers.app_user_serializer import (
    AppUserReadSerializer,
    AppUserWriteSerializer,
)
from core.services.app_user_service import (
    list_app_users,
    get_app_user,
    create_app_user,
    partial_update_app_user,
    delete_app_user,
)

logger = logging.getLogger(__name__)


class AppUserListView(APIView):
    def get(self, request):
        try:
            logger.info("AppUserListView GET started")

            dtos = list_app_users()

            logger.info("AppUserListView GET success | count=%s", len(dtos))
            return Response(
                AppUserReadSerializer(dtos, many=True).data,
                status=status.HTTP_200_OK,
            )

        except ApiException as exc:
            logger.warning("AppUserListView GET api error | code=%s | detail=%s", exc.code, exc.detail)
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except Exception:
            logger.exception("AppUserListView GET unexpected error")
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AppUserDetailView(APIView):
    def get(self, request, app_user_id: int):
        try:
            logger.info("AppUserDetailView GET started | app_user_id=%s", app_user_id)

            dto = get_app_user(app_user_id)

            logger.info("AppUserDetailView GET success | app_user_id=%s", app_user_id)
            return Response(
                AppUserReadSerializer(dto).data,
                status=status.HTTP_200_OK,
            )

        except ApiException as exc:
            logger.warning(
                "AppUserDetailView GET api error | app_user_id=%s | code=%s | detail=%s",
                app_user_id,
                exc.code,
                exc.detail,
            )
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except Exception:
            logger.exception("AppUserDetailView GET unexpected error | app_user_id=%s", app_user_id)
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AppUserCreateView(APIView):
    def post(self, request):
        try:
            logger.info("AppUserCreateView POST started | payload_keys=%s", list(request.data.keys()))

            serializer = AppUserWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            dto = serializer.to_upsert_dto()
            created = create_app_user(dto)

            logger.info("AppUserCreateView POST success | app_user_id=%s", created.id)
            return Response(
                AppUserReadSerializer(created).data,
                status=status.HTTP_201_CREATED,
            )

        except ApiException as exc:
            logger.warning("AppUserCreateView POST api error | code=%s | detail=%s", exc.code, exc.detail)
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except DRFValidationError as exc:
            logger.warning("AppUserCreateView POST validation error | errors=%s", exc.detail)
            return build_error_response(
                ErrorCodes.VALIDATION_ERROR,
                ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
                status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            logger.exception("AppUserCreateView POST unexpected error")
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class AppUserPartialUpdateView(APIView):
    def patch(self, request, app_user_id: int):
        try:
            logger.info(
                "AppUserPartialUpdateView PATCH started | app_user_id=%s | payload_keys=%s",
                app_user_id,
                list(request.data.keys()),
            )

            serializer = AppUserWriteSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            fields = serializer.validated_data
            updated = partial_update_app_user(app_user_id, fields)

            logger.info(
                "AppUserPartialUpdateView PATCH success | app_user_id=%s | updated_fields=%s",
                app_user_id,
                list(fields.keys()),
            )
            return Response(
                AppUserReadSerializer(updated).data,
                status=status.HTTP_200_OK,
            )

        except ApiException as exc:
            logger.warning(
                "AppUserPartialUpdateView PATCH api error | app_user_id=%s | code=%s | detail=%s",
                app_user_id,
                exc.code,
                exc.detail,
            )
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except DRFValidationError as exc:
            logger.warning(
                "AppUserPartialUpdateView PATCH validation error | app_user_id=%s | errors=%s",
                app_user_id,
                exc.detail,
            )
            return build_error_response(
                ErrorCodes.VALIDATION_ERROR,
                ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
                status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            logger.exception("AppUserPartialUpdateView PATCH unexpected error | app_user_id=%s", app_user_id)
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AppUserDeleteView(APIView):
    def delete(self, request, app_user_id: int):
        try:
            logger.info("AppUserDeleteView DELETE started | app_user_id=%s", app_user_id)

            delete_app_user(app_user_id)

            logger.info("AppUserDeleteView DELETE success | app_user_id=%s", app_user_id)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ApiException as exc:
            logger.warning(
                "AppUserDeleteView DELETE api error | app_user_id=%s | code=%s | detail=%s",
                app_user_id,
                exc.code,
                exc.detail,
            )
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except Exception:
            logger.exception("AppUserDeleteView DELETE unexpected error | app_user_id=%s", app_user_id)
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
