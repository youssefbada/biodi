from core.models import AppUser
from rest_framework.test import APIClient

class AuthenticatedUserMixin:
    """
    Mixin à ajouter dans chaque APITestCase.
    Crée un user en base et injecte la session OIDC.
    """
    def setUp(self):
        self.client = APIClient()  # ← ajout
        self.app_user = AppUser.objects.create(
            nni="a30481",
            first_name="Test",
            last_name="User",
            email="test@edf.fr",
            role="READ_ONLY",
            is_active=True,
        )
        self._inject_session(nni="a30481")

    def _inject_session(self, nni):
        session = self.client.session
        session["user"] = {"nni": nni}
        session.save()

    def set_admin(self):
        """Passer en mode admin pour un test spécifique."""
        self.app_user.role = "ADMIN"
        self.app_user.save()


class AuthenticatedAdminMixin(AuthenticatedUserMixin):
    def setUp(self):
        self.client = APIClient()  # ← ajout
        self.app_user = AppUser.objects.create(
            nni="admin01",
            first_name="Admin",
            last_name="User",
            email="admin@edf.fr",
            role="ADMIN",
            is_active=True,
        )
        self._inject_session(nni="admin01")