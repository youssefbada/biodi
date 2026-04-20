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

from core.serializers.dynamic_query_serializer import QueryBuilderRequestSerializer
from core.services.dynamic_query_service import (
    get_query_builder_metadata,
    execute_query_builder,
)

logger = logging.getLogger(__name__)

@method_decorator(require_session_user, name="dispatch")
class QueryBuilderMetadataView(APIView):
    def get(self, request):
        try:
            logger.info("QueryBuilderMetadataView GET started")

            data = get_query_builder_metadata()

            logger.info("QueryBuilderMetadataView GET success")

            return Response(data, status=status.HTTP_200_OK)

        except ApiException as exc:
            logger.warning(
                "QueryBuilderMetadataView GET api error | code=%s | detail=%s",
                exc.code,
                exc.detail,
            )
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except Exception:
            logger.exception("QueryBuilderMetadataView GET unexpected error")
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@method_decorator(require_session_user, name="dispatch")
class QueryBuilderExecuteView(APIView):
    def post(self, request):
        try:
            logger.info(
                "QueryBuilderExecuteView POST started | payload_keys=%s",
                list(request.data.keys()),
            )

            serializer = QueryBuilderRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print(serializer.validated_data)
            result = execute_query_builder(serializer.validated_data)

            logger.info(
                "QueryBuilderExecuteView POST success | row_count=%s",
                result["count"],
            )
            return Response(result, status=status.HTTP_200_OK)

        except ApiException as exc:
            logger.warning(
                "QueryBuilderExecuteView POST api error | code=%s | detail=%s",
                exc.code,
                exc.detail,
            )
            return build_error_response(exc.code, exc.detail, exc.status_code)

        except DRFValidationError as exc:
            logger.warning(
                "QueryBuilderExecuteView POST validation error | errors=%s",
                exc.detail,
            )
            return build_error_response(
                ErrorCodes.VALIDATION_ERROR,
                ERROR_MESSAGES[ErrorCodes.VALIDATION_ERROR],
                status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            logger.exception("QueryBuilderExecuteView POST unexpected error")
            return build_error_response(
                ErrorCodes.INTERNAL_ERROR,
                ERROR_MESSAGES[ErrorCodes.INTERNAL_ERROR],
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
