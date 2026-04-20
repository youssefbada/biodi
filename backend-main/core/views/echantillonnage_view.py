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

from core.serializers.echantillonnage_serializer import (
  EchantillonnageReadSerializer,
  EchantillonnageWriteSerializer,
)
from core.services.echantillonnage_service import (
  list_echantillonnages,
  get_echantillonnage,
  create_echantillonnage,
  update_echantillonnage,
  partial_update_echantillonnage,
  delete_echantillonnage,
)

logger = logging.getLogger(__name__)

@method_decorator(require_session_user, name="dispatch")
class EchantillonnageListView(APIView):
  def get(self, request):
    try:
      logger.info("EchantillonnageListView GET started")

      dtos = list_echantillonnages()

      logger.info("EchantillonnageListView GET success | count=%s", len(dtos))
      return Response(
        EchantillonnageReadSerializer(dtos, many=True).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "EchantillonnageListView GET api error | code=%s | detail=%s",
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("EchantillonnageListView GET unexpected error")
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_session_user, name="dispatch")
class EchantillonnageDetailView(APIView):
  def get(self, request, echantillonnage_id: int):
    try:
      logger.info("EchantillonnageDetailView GET started | echantillonnage_id=%s", echantillonnage_id)

      dto = get_echantillonnage(echantillonnage_id)

      logger.info("EchantillonnageDetailView GET success | echantillonnage_id=%s", echantillonnage_id)
      return Response(
        EchantillonnageReadSerializer(dto).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "EchantillonnageDetailView GET api error | echantillonnage_id=%s | code=%s | detail=%s",
        echantillonnage_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("EchantillonnageDetailView GET unexpected error | echantillonnage_id=%s", echantillonnage_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class EchantillonnageCreateView(APIView):
  def post(self, request):
    try:
      logger.info(
        "EchantillonnageCreateView POST started | payload_keys=%s",
        list(request.data.keys()),
      )

      serializer = EchantillonnageWriteSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      dto = serializer.to_upsert_dto()
      created = create_echantillonnage(dto)

      logger.info("EchantillonnageCreateView POST success | id=%s", created.id_echantillonnage)
      return Response(
        EchantillonnageReadSerializer(created).data,
        status=status.HTTP_201_CREATED,
      )

    except ApiException as exc:
      logger.warning(
        "EchantillonnageCreateView POST api error | code=%s | detail=%s",
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "EchantillonnageCreateView POST validation error | errors=%s",
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("EchantillonnageCreateView POST unexpected error")
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class EchantillonnageUpdateView(APIView):
  def put(self, request, echantillonnage_id: int):
    try:
      logger.info(
        "EchantillonnageUpdateView PUT started | echantillonnage_id=%s | payload_keys=%s",
        echantillonnage_id,
        list(request.data.keys()),
      )

      serializer = EchantillonnageWriteSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      dto = serializer.to_upsert_dto()
      updated = update_echantillonnage(echantillonnage_id, dto)

      logger.info("EchantillonnageUpdateView PUT success | echantillonnage_id=%s", echantillonnage_id)
      return Response(
        EchantillonnageReadSerializer(updated).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "EchantillonnageUpdateView PUT api error | echantillonnage_id=%s | code=%s | detail=%s",
        echantillonnage_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "EchantillonnageUpdateView PUT validation error | echantillonnage_id=%s | errors=%s",
        echantillonnage_id,
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("EchantillonnageUpdateView PUT unexpected error | echantillonnage_id=%s", echantillonnage_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class EchantillonnagePartialUpdateView(APIView):
  def patch(self, request, echantillonnage_id: int):
    try:
      logger.info(
        "EchantillonnagePartialUpdateView PATCH started | echantillonnage_id=%s | payload_keys=%s",
        echantillonnage_id,
        list(request.data.keys()),
      )

      serializer = EchantillonnageWriteSerializer(data=request.data, partial=True)
      serializer.is_valid(raise_exception=True)

      fields = serializer.validated_data
      updated = partial_update_echantillonnage(echantillonnage_id, fields)

      logger.info(
        "EchantillonnagePartialUpdateView PATCH success | echantillonnage_id=%s | updated_fields=%s",
        echantillonnage_id,
        list(fields.keys()),
      )
      return Response(
        EchantillonnageReadSerializer(updated).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "EchantillonnagePartialUpdateView PATCH api error | echantillonnage_id=%s | code=%s | detail=%s",
        echantillonnage_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "EchantillonnagePartialUpdateView PATCH validation error | echantillonnage_id=%s | errors=%s",
        echantillonnage_id,
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("EchantillonnagePartialUpdateView PATCH unexpected error | echantillonnage_id=%s", echantillonnage_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class EchantillonnageDeleteView(APIView):
  def delete(self, request, echantillonnage_id: int):
    try:
      logger.info("EchantillonnageDeleteView DELETE started | echantillonnage_id=%s", echantillonnage_id)

      delete_echantillonnage(echantillonnage_id)

      logger.info("EchantillonnageDeleteView DELETE success | echantillonnage_id=%s", echantillonnage_id)
      return Response(status=status.HTTP_204_NO_CONTENT)

    except ApiException as exc:
      logger.warning(
        "EchantillonnageDeleteView DELETE api error | echantillonnage_id=%s | code=%s | detail=%s",
        echantillonnage_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("EchantillonnageDeleteView DELETE unexpected error | echantillonnage_id=%s", echantillonnage_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )
