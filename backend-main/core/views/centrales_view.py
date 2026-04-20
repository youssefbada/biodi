from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError as DRFValidationError
import logging
from core.utils.api_utils import build_error_response
from core.constants.error_codes import ErrorCodes
from core.constants.error_messages import ERROR_MESSAGES
from core.exceptions.api_exceptions import ApiException
from django.utils.decorators import method_decorator
from auth_oidc.decorators import require_session_user, require_admin_user

from core.serializers.centrales_serializer import (
    CentraleReadSerializer,
    CentraleWriteSerializer,
)
from core.services.centrales_service import (
    list_centrales,
    get_centrale,
    create_centrale,
    update_centrale,
    partial_update_centrale,
    delete_centrale,
)

try:
    from drf_yasg.utils import swagger_auto_schema
except Exception:

    def swagger_auto_schema(*args, **kwargs):
        def deco(fn):
            return fn

        return deco

logger = logging.getLogger(__name__)

@method_decorator(require_session_user, name="dispatch")
class CentraleListView(APIView):
    """
    GET /centrales/
    """

    @swagger_auto_schema(
        operation_description="List centrales.",
        responses={200: CentraleReadSerializer(many=True)},
    )
    def get(self, request):
        try:
            logger.info(
              "CentraleListView GET started | user=%s",
              request.app_user.nni,
            )

            dtos = list_centrales()

            logger.info(
                "CentraleListView GET success | user=%s | count=%s",
                request.app_user.nni,
                len(dtos),
            )

            return Response(
                CentraleReadSerializer(dtos, many=True).data,
                status=status.HTTP_200_OK,
            )

        except ApiException as exc:
            logger.warning(
                "CentraleListView GET Api error| user=%s | code=%s | detail=%s",
                request.app_user.nni,
                exc.code,
                exc.detail,
            )
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except Exception:
            logger.exception(
                "CentraleListView GET unexpected error",
                request.app_user.nni,
            )
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@method_decorator(require_session_user, name="dispatch")
class CentraleDetailView(APIView):
    """
    GET /centrales/{id}/
    """
    @swagger_auto_schema(
        operation_description="Get centrale by id.",
        responses={200: CentraleReadSerializer()},
    )
    def get(self, request, centrale_id: int):
        try:
            logger.info(
                "CentraleDetailView GET started | user=%s | centrale_id=%s",
                request.app_user.nni,
                centrale_id,
            )

            dto = get_centrale(centrale_id)

            logger.info(
              "CentraleDetailView GET success | user=%s | centrale_id=%s",
              request.app_user.nni,
              centrale_id,
            )

            return Response(
                CentraleReadSerializer(dto).data,
                status=status.HTTP_200_OK,
            )

        except ApiException as exc:
            logger.warning(
              "CentraleDetailView GET Api error | user=%s | centrale_id=%s | code=%s | detail=%s",
              request.app_user.nni,
              centrale_id,
              exc.code,
              exc.detail,
            )
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except Exception:
            logger.exception(
              "CentraleDetailView GET unexpected error | user=%s | centrale_id=%s",
              request.app_user.nni,
              centrale_id,
            )
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@method_decorator(require_admin_user, name="dispatch")
class CentraleCreateView(APIView):
    """
    POST /centrales/create/
    """
    @swagger_auto_schema(
        operation_description="Create centrale.",
        request_body=CentraleWriteSerializer,
        responses={201: CentraleReadSerializer()},
    )
    def post(self, request):
        try:
            logger.info(
                "CentraleCreateView POST started | user=%s | payload_keys=%s",
                request.app_user.nni,
                list(request.data.keys()),
            )

            serializer = CentraleWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            dto = serializer.to_upsert_dto()
            created = create_centrale(dto)

            logger.info(
                "CentraleCreateView POST success | user=%s | centrale_id=%s | code_nom=%s",
                request.app_user.nni,
                created.id,
                created.code_nom,
            )

            return Response(
                CentraleReadSerializer(created).data,
                status=status.HTTP_201_CREATED,
            )

        except ApiException as exc:
            logger.warning(
                "CentraleCreateView POST Api error | user=%s | code=%s | detail=%s",
                request.app_user.nni,
                exc.code,
                exc.detail,
            )
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except DRFValidationError as exc:
            logger.warning(
                "CentraleCreateView POST validation error | user=%s | errors=%s",
                request.app_user.nni,
                exc.detail,
            )
            return build_error_response(
                ErrorCodes.VALIDATION_ERROR,
                ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
                status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            logger.exception(
                "CentraleCreateView POST unexpected error | user=%s",
                request.app_user.nni,
            )
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@method_decorator(require_admin_user, name="dispatch")
class CentraleUpdateView(APIView):
    """
    PUT /centrales/{id}/update/
    """

    @swagger_auto_schema(
        operation_description="Update centrale.",
        request_body=CentraleWriteSerializer,
        responses={200: CentraleReadSerializer()},
    )
    def put(self, request, centrale_id: int):
        try:
            logger.info(
              "CentraleUpdateView PUT started | user=%s | centrale_id=%s | payload_keys=%s",
              request.app_user.nni,
              centrale_id,
              list(request.data.keys()),
            )

            serializer = CentraleWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            dto = serializer.to_upsert_dto()
            updated = update_centrale(centrale_id, dto)

            logger.info(
              "CentraleUpdateView PUT success | user=%s | centrale_id=%s | code_nom=%s",
              request.app_user.nni,
              centrale_id,
              updated.code_nom,
            )

            return Response(
                CentraleReadSerializer(updated).data,
                status=status.HTTP_200_OK,
            )

        except ApiException as exc:
            logger.warning(
              "CentraleUpdateView PUT Api error | user=%s | centrale_id=%s | code=%s | detail=%s",
              request.app_user.nni,
              centrale_id,
              exc.code,
              exc.detail,
            )
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except DRFValidationError as exc:
            logger.warning(
              "CentraleUpdateView PUT validation error | user=%s | centrale_id=%s | errors=%s",
              request.app_user.nni,
              centrale_id,
              exc.detail,
            )
            return build_error_response(
                ErrorCodes.VALIDATION_ERROR,
                ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
                status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            logger.exception(
              "CentraleUpdateView PUT unexpected error | user=%s | centrale_id=%s",
              request.app_user.nni,
              centrale_id,
            )
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@method_decorator(require_admin_user, name="dispatch")
class CentralePartialUpdateView(APIView):
    """
    PATCH /centrales/{id}/partial/
    """

    @swagger_auto_schema(
        operation_description="Partial update centrale.",
        request_body=CentraleWriteSerializer,
        responses={200: CentraleReadSerializer()},
    )
    def patch(self, request, centrale_id: int):

        try:
            logger.info(
              "CentralePartialUpdateView PATCH started | user=%s | centrale_id=%s | payload_keys=%s",
              request.app_user.nni,
              centrale_id,
              list(request.data.keys()),
            )

            serializer = CentraleWriteSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            fields = serializer.validated_data
            updated = partial_update_centrale(centrale_id, fields)

            logger.info(
              "CentralePartialUpdateView PATCH success | user=%s | centrale_id=%s | updated_fields=%s",
              request.app_user.nni,
              centrale_id,
              list(fields.keys()),
            )

            return Response(
                CentraleReadSerializer(updated).data,
                status=status.HTTP_200_OK,
            )

        except ApiException as exc:
            logger.warning(
              "CentralePartialUpdateView PATCH Api error | user=%s | centrale_id=%s | code=%s | detail=%s",
              request.app_user.nni,
              centrale_id,
              exc.code,
              exc.detail,
            )
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except DRFValidationError as exc:
            logger.warning(
              "CentralePartialUpdateView PATCH validation error | user=%s | centrale_id=%s | errors=%s",
              request.app_user.nni,
              centrale_id,
              exc.detail,
            )
            return build_error_response(
                ErrorCodes.VALIDATION_ERROR,
                ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
                status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            logger.exception(
              "CentralePartialUpdateView PATCH unexpected error | user=%s | centrale_id=%s",
              request.app_user.nni,
              centrale_id,
            )
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@method_decorator(require_admin_user, name="dispatch")
class CentraleDeleteView(APIView):
    """
    DELETE /centrales/{id}/delete/
    """

    @swagger_auto_schema(
        operation_description="Delete centrale.",
        responses={204: "No Content"},
    )
    def delete(self, request, centrale_id: int):

        try:
            logger.info(
              "CentraleDeleteView DELETE started | user=%s | centrale_id=%s",
              request.app_user.nni,
              centrale_id,
            )

            delete_centrale(centrale_id)

            logger.info(
              "CentraleDeleteView DELETE success | user=%s | centrale_id=%s",
              request.app_user.nni,
              centrale_id,
            )

            return Response(status=status.HTTP_204_NO_CONTENT)

        except ApiException as exc:
            logger.warning(
              "CentraleDeleteView DELETE Api error | user=%s | centrale_id=%s | code=%s | detail=%s",
              request.app_user.nni,
              centrale_id,
              exc.code,
              exc.detail,
            )
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except Exception:
            logger.exception(
              "CentraleDeleteView DELETE unexpected error | user=%s | centrale_id=%s",
              request.app_user.nni,
              centrale_id,
            )
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
