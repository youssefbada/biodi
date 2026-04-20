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

from core.serializers.non_poissons_serializer import (
  NonPoissonReadSerializer,
  NonPoissonWriteSerializer,
)
from core.services.non_poissons_service import (
  list_non_poissons,
  get_non_poisson,
  create_non_poisson,
  update_non_poisson,
  partial_update_non_poisson,
  delete_non_poisson,
)

logger = logging.getLogger(__name__)

@method_decorator(require_session_user, name="dispatch")
class NonPoissonListView(APIView):
  def get(self, request):
    try:
      logger.info("NonPoissonListView GET started")

      dtos = list_non_poissons()

      logger.info("NonPoissonListView GET success | count=%s", len(dtos))
      return Response(
        NonPoissonReadSerializer(dtos, many=True).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "NonPoissonListView GET api error | code=%s | detail=%s",
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("NonPoissonListView GET unexpected error")
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_session_user, name="dispatch")

class NonPoissonDetailView(APIView):
  def get(self, request, non_poisson_id: int):
    try:
      logger.info("NonPoissonDetailView GET started | non_poisson_id=%s", non_poisson_id)

      dto = get_non_poisson(non_poisson_id)

      logger.info("NonPoissonDetailView GET success | non_poisson_id=%s", non_poisson_id)
      return Response(
        NonPoissonReadSerializer(dto).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "NonPoissonDetailView GET api error | non_poisson_id=%s | code=%s | detail=%s",
        non_poisson_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("NonPoissonDetailView GET unexpected error | non_poisson_id=%s", non_poisson_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class NonPoissonCreateView(APIView):
  def post(self, request):
    try:
      logger.info(
        "NonPoissonCreateView POST started | payload_keys=%s",
        list(request.data.keys()),
      )

      serializer = NonPoissonWriteSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      dto = serializer.to_upsert_dto()
      created = create_non_poisson(dto)

      logger.info("NonPoissonCreateView POST success | non_poisson_id=%s", created.id_non_poisson)
      return Response(
        NonPoissonReadSerializer(created).data,
        status=status.HTTP_201_CREATED,
      )

    except ApiException as exc:
      logger.warning(
        "NonPoissonCreateView POST api error | code=%s | detail=%s",
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "NonPoissonCreateView POST validation error | errors=%s",
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("NonPoissonCreateView POST unexpected error")
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class NonPoissonUpdateView(APIView):
  def put(self, request, non_poisson_id: int):
    try:
      logger.info(
        "NonPoissonUpdateView PUT started | non_poisson_id=%s | payload_keys=%s",
        non_poisson_id,
        list(request.data.keys()),
      )

      serializer = NonPoissonWriteSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      dto = serializer.to_upsert_dto()
      updated = update_non_poisson(non_poisson_id, dto)

      logger.info("NonPoissonUpdateView PUT success | non_poisson_id=%s", non_poisson_id)
      return Response(
        NonPoissonReadSerializer(updated).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "NonPoissonUpdateView PUT api error | non_poisson_id=%s | code=%s | detail=%s",
        non_poisson_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "NonPoissonUpdateView PUT validation error | non_poisson_id=%s | errors=%s",
        non_poisson_id,
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("NonPoissonUpdateView PUT unexpected error | non_poisson_id=%s", non_poisson_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class NonPoissonPartialUpdateView(APIView):
  def patch(self, request, non_poisson_id: int):
    try:
      logger.info(
        "NonPoissonPartialUpdateView PATCH started | non_poisson_id=%s | payload_keys=%s",
        non_poisson_id,
        list(request.data.keys()),
      )

      serializer = NonPoissonWriteSerializer(data=request.data, partial=True)
      serializer.is_valid(raise_exception=True)

      fields = serializer.validated_data
      updated = partial_update_non_poisson(non_poisson_id, fields)

      logger.info(
        "NonPoissonPartialUpdateView PATCH success | non_poisson_id=%s | updated_fields=%s",
        non_poisson_id,
        list(fields.keys()),
      )
      return Response(
        NonPoissonReadSerializer(updated).data,
        status=status.HTTP_200_OK,
      )

    except ApiException as exc:
      logger.warning(
        "NonPoissonPartialUpdateView PATCH api error | non_poisson_id=%s | code=%s | detail=%s",
        non_poisson_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except DRFValidationError as exc:
      logger.warning(
        "NonPoissonPartialUpdateView PATCH validation error | non_poisson_id=%s | errors=%s",
        non_poisson_id,
        exc.detail,
      )
      return build_error_response(
        ErrorCodes.VALIDATION_ERROR,
        ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
        status.HTTP_400_BAD_REQUEST,
      )

    except Exception:
      logger.exception("NonPoissonPartialUpdateView PATCH unexpected error | non_poisson_id=%s", non_poisson_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )

@method_decorator(require_admin_user, name="dispatch")
class NonPoissonDeleteView(APIView):
  def delete(self, request, non_poisson_id: int):
    try:
      logger.info("NonPoissonDeleteView DELETE started | non_poisson_id=%s", non_poisson_id)

      delete_non_poisson(non_poisson_id)

      logger.info("NonPoissonDeleteView DELETE success | non_poisson_id=%s", non_poisson_id)
      return Response(status=status.HTTP_204_NO_CONTENT)

    except ApiException as exc:
      logger.warning(
        "NonPoissonDeleteView DELETE api error | non_poisson_id=%s | code=%s | detail=%s",
        non_poisson_id,
        exc.code,
        exc.detail,
      )
      return build_error_response(exc.code, exc.detail, exc.status_code)

    except Exception:
      logger.exception("NonPoissonDeleteView DELETE unexpected error | non_poisson_id=%s", non_poisson_id)
      return build_error_response(
        ErrorCodes.INTERNAL_ERROR,
        ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
        status.HTTP_500_INTERNAL_SERVER_ERROR,
      )
