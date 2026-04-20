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

from core.serializers.poissons_serializer import (
  PoissonReadSerializer,
  PoissonWriteSerializer,
)
from core.services.poissons_service import (
  list_poissons,
  get_poisson,
  create_poisson,
  update_poisson,
  partial_update_poisson,
  delete_poisson,
)

logger = logging.getLogger(__name__)

@method_decorator(require_session_user, name="dispatch")
class PoissonListView(APIView):
  def get(self, request):
    try:
      logger.info("PoissonListView GET started")

      dtos = list_poissons()

      logger.info("PoissonListView GET success | count=%s", len(dtos))
      return Response(
        PoissonReadSerializer(dtos, many=True).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "PoissonListView GET api error | code=%s | detail=%s",
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("PoissonListView GET unexpected error")
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_session_user, name="dispatch")
class PoissonDetailView(APIView):
  def get(self, request, poisson_id: int):
    try:
      logger.info("PoissonDetailView GET started | poisson_id=%s", poisson_id)

      dto = get_poisson(poisson_id)

      logger.info("PoissonDetailView GET success | poisson_id=%s", poisson_id)
      return Response(
        PoissonReadSerializer(dto).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "PoissonDetailView GET api error | poisson_id=%s | code=%s | detail=%s",
        poisson_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("PoissonDetailView GET unexpected error | poisson_id=%s", poisson_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class PoissonCreateView(APIView):
  def post(self, request):
    try:
      logger.info(
        "PoissonCreateView POST started | payload_keys=%s",
        list(request.data.keys()),
      )

      serializer = PoissonWriteSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      dto = serializer.to_upsert_dto()
      created = create_poisson(dto)

      logger.info("PoissonCreateView POST success | poisson_id=%s", created.id_poisson)
      return Response(
        PoissonReadSerializer(created).data,
        status=status.HTTP_201_CREATED,
      )

    except ApiException as exc:
      logger.warning(
        "PoissonCreateView POST api error | code=%s | detail=%s",
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "PoissonCreateView POST validation error | errors=%s",
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("PoissonCreateView POST unexpected error")
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class PoissonUpdateView(APIView):
  def put(self, request, poisson_id: int):
    try:
      logger.info(
        "PoissonUpdateView PUT started | poisson_id=%s | payload_keys=%s",
        poisson_id,
        list(request.data.keys()),
      )

      serializer = PoissonWriteSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      dto = serializer.to_upsert_dto()
      updated = update_poisson(poisson_id, dto)

      logger.info("PoissonUpdateView PUT success | poisson_id=%s", poisson_id)
      return Response(
        PoissonReadSerializer(updated).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "PoissonUpdateView PUT api error | poisson_id=%s | code=%s | detail=%s",
        poisson_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "PoissonUpdateView PUT validation error | poisson_id=%s | errors=%s",
        poisson_id,
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("PoissonUpdateView PUT unexpected error | poisson_id=%s", poisson_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class PoissonPartialUpdateView(APIView):
  def patch(self, request, poisson_id: int):
    try:
      logger.info(
        "PoissonPartialUpdateView PATCH started | poisson_id=%s | payload_keys=%s",
        poisson_id,
        list(request.data.keys()),
      )

      serializer = PoissonWriteSerializer(data=request.data, partial=True)
      serializer.is_valid(raise_exception=True)

      fields = serializer.validated_data
      updated = partial_update_poisson(poisson_id, fields)

      logger.info(
        "PoissonPartialUpdateView PATCH success | poisson_id=%s | updated_fields=%s",
        poisson_id,
        list(fields.keys()),
      )
      return Response(
        PoissonReadSerializer(updated).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "PoissonPartialUpdateView PATCH api error | poisson_id=%s | code=%s | detail=%s",
        poisson_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "PoissonPartialUpdateView PATCH validation error | poisson_id=%s | errors=%s",
        poisson_id,
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("PoissonPartialUpdateView PATCH unexpected error | poisson_id=%s", poisson_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class PoissonDeleteView(APIView):
  def delete(self, request, poisson_id: int):
    try:
      logger.info("PoissonDeleteView DELETE started | poisson_id=%s", poisson_id)

      delete_poisson(poisson_id)

      logger.info("PoissonDeleteView DELETE success | poisson_id=%s", poisson_id)
      return Response(status=status.HTTP_204_NO_CONTENT)

    except ApiException as exc:
      logger.warning(
        "PoissonDeleteView DELETE api error | poisson_id=%s | code=%s | detail=%s",
        poisson_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("PoissonDeleteView DELETE unexpected error | poisson_id=%s", poisson_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )
