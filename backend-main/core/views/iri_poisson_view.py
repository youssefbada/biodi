from datetime import datetime

from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.serializers.iri_poisson_serializer import IriPoissonResponseSerializer
from core.services.iri_poisson_service import IriPoissonService, IriPoissonServiceError
from auth_oidc.decorators import require_session_user


@method_decorator(require_session_user, name="dispatch")
class IriPoissonView(APIView):
    """
    GET /api/iri/poissons/?site_id=BLA&date=1984-06-01

    - site_id: string
    - date: YYYY-MM-DD (date du suivi)
    """

    def get(self, request):
        site_id = request.query_params.get("site_id")
        date_str = request.query_params.get("date")

        if not site_id or not date_str:
            return Response(
                {"detail": "Paramètres requis: site_id, date (YYYY-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            suivi_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"detail": "Format de date invalide. Attendu: YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = IriPoissonService()
        try:
            payload = service.compute(site_id=site_id, suivi_date=suivi_date)
        except IriPoissonServiceError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = IriPoissonResponseSerializer(payload)
        return Response(serializer.data, status=status.HTTP_200_OK)

# curl "http://127.0.0.1:8000/api/iri/poissons/?site_id=BLA&date=1984-06-01"
