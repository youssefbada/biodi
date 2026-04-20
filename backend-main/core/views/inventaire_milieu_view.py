import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.utils.decorators import method_decorator
from auth_oidc.decorators import require_session_user, require_admin_user

from core.utils.api_utils import build_error_response
from core.constants.error_codes import ErrorCodes
from core.constants.error_messages import ERROR_MESSAGES
from core.exceptions.api_exceptions import ApiException

from core.serializers.inventaire_milieu_serializer import (
  InventaireMilieuReadSerializer,
  InventaireMilieuWriteSerializer,
)
from core.services.inventaire_milieu_service import (
  list_inventaires_milieu,
  get_inventaire_milieu,
  create_inventaire_milieu,
  update_inventaire_milieu,
  partial_update_inventaire_milieu,
  delete_inventaire_milieu,
)

logger = logging.getLogger(__name__)

@method_decorator(require_session_user, name="dispatch")
class InventaireMilieuListView(APIView):
  def get(self, request):
    try:
      logger.info("InventaireMilieuListView GET started")

      dtos = list_inventaires_milieu()

      logger.info("InventaireMilieuListView GET success | count=%s", len(dtos))
      return Response(
        InventaireMilieuReadSerializer(dtos, many=True).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "InventaireMilieuListView GET api error | code=%s | detail=%s",
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("InventaireMilieuListView GET unexpected error")
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_session_user, name="dispatch")
class InventaireMilieuDetailView(APIView):
  def get(self, request, inventaire_id: int):
    try:
      logger.info("InventaireMilieuDetailView GET started | inventaire_id=%s", inventaire_id)

      dto = get_inventaire_milieu(inventaire_id)

      logger.info("InventaireMilieuDetailView GET success | inventaire_id=%s", inventaire_id)
      return Response(
        InventaireMilieuReadSerializer(dto).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "InventaireMilieuDetailView GET api error | inventaire_id=%s | code=%s | detail=%s",
        inventaire_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("InventaireMilieuDetailView GET unexpected error | inventaire_id=%s", inventaire_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class InventaireMilieuCreateView(APIView):
  def post(self, request):
    try:
      logger.info(
        "InventaireMilieuCreateView POST started | payload_keys=%s",
        list(request.data.keys()),
      )

      serializer = InventaireMilieuWriteSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      dto = serializer.to_upsert_dto()
      created = create_inventaire_milieu(dto)

      logger.info("InventaireMilieuCreateView POST success | inventaire_id=%s", created.id_inventaire)
      return Response(
        InventaireMilieuReadSerializer(created).data,
        status=status.HTTP_201_CREATED,
      )

    except ApiException as exc:
      logger.warning(
        "InventaireMilieuCreateView POST api error | code=%s | detail=%s",
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "InventaireMilieuCreateView POST validation error | errors=%s",
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("InventaireMilieuCreateView POST unexpected error")
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class InventaireMilieuUpdateView(APIView):
  def put(self, request, inventaire_id: int):
    try:
      logger.info(
        "InventaireMilieuUpdateView PUT started | inventaire_id=%s | payload_keys=%s",
        inventaire_id,
        list(request.data.keys()),
      )

      serializer = InventaireMilieuWriteSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      dto = serializer.to_upsert_dto()
      updated = update_inventaire_milieu(inventaire_id, dto)

      logger.info("InventaireMilieuUpdateView PUT success | inventaire_id=%s", inventaire_id)
      return Response(
        InventaireMilieuReadSerializer(updated).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "InventaireMilieuUpdateView PUT api error | inventaire_id=%s | code=%s | detail=%s",
        inventaire_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "InventaireMilieuUpdateView PUT validation error | inventaire_id=%s | errors=%s",
        inventaire_id,
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("InventaireMilieuUpdateView PUT unexpected error | inventaire_id=%s", inventaire_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class InventaireMilieuPartialUpdateView(APIView):
  def patch(self, request, inventaire_id: int):
    try:
      logger.info(
        "InventaireMilieuPartialUpdateView PATCH started | inventaire_id=%s | payload_keys=%s",
        inventaire_id,
        list(request.data.keys()),
      )

      serializer = InventaireMilieuWriteSerializer(data=request.data, partial=True)
      serializer.is_valid(raise_exception=True)

      fields = serializer.validated_data
      updated = partial_update_inventaire_milieu(inventaire_id, fields)

      logger.info(
        "InventaireMilieuPartialUpdateView PATCH success | inventaire_id=%s | updated_fields=%s",
        inventaire_id,
        list(fields.keys()),
      )
      return Response(
        InventaireMilieuReadSerializer(updated).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "InventaireMilieuPartialUpdateView PATCH api error | inventaire_id=%s | code=%s | detail=%s",
        inventaire_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "InventaireMilieuPartialUpdateView PATCH validation error | inventaire_id=%s | errors=%s",
        inventaire_id,
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("InventaireMilieuPartialUpdateView PATCH unexpected error | inventaire_id=%s", inventaire_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class InventaireMilieuDeleteView(APIView):
  def delete(self, request, inventaire_id: int):
    try:
      logger.info("InventaireMilieuDeleteView DELETE started | inventaire_id=%s", inventaire_id)

      delete_inventaire_milieu(inventaire_id)

      logger.info("InventaireMilieuDeleteView DELETE success | inventaire_id=%s", inventaire_id)
      return Response(status=status.HTTP_204_NO_CONTENT)

    except ApiException as exc:
      logger.warning(
        "InventaireMilieuDeleteView DELETE api error | inventaire_id=%s | code=%s | detail=%s",
        inventaire_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("InventaireMilieuDeleteView DELETE unexpected error | inventaire_id=%s", inventaire_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )
