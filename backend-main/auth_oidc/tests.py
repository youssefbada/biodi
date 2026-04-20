import time
from unittest.mock import patch, Mock, MagicMock

from django.test import TestCase, override_settings, Client
from rest_framework.test import APIClient
from core.models import AppUser


@override_settings(
    SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False,
    OIDC_GARDIAN={
        "BASE_URL": "https://fake-gardian.example.com",
        "CLIENT_ID": "fake-client-id",
        "CLIENT_SECRET": "fake-secret",
        "REDIRECT_URI": "https://fake.example.com/callback",
        "POST_LOGOUT_REDIRECT_URI": "https://fake.example.com/logout",
        "SCOPE": "openid",
        "ACR_VALUES": "sesameEDF",
        "GRANT_TYPE": "authorization_code",
        "ALLOWED_ID_TOKEN_ALGS": "RS256",
        "STATE_TTL_SECONDS": 300,
        "SESSION_FALLBACK_TTL_SECONDS": 3600,
    }
)
class OIDCTests(TestCase):

    def setUp(self):
        self.client_api = APIClient()
        self.app_user = AppUser.objects.create(
            nni="testuser",
            email="test@edf.fr",
            role="READ_ONLY",
            is_active=True,
        )

    def _set_session(self, client, data: dict):
        session = client.session
        for k, v in data.items():
            session[k] = v
        session.save()

    # LOGIN
    @patch("auth_oidc.oidc_service.GardianOIDCService.build_authorize_url")
    @patch("auth_oidc.oidc_service.GardianOIDCService.generate_nonce")
    @patch("auth_oidc.oidc_service.GardianOIDCService.generate_state")
    def test_login_redirects_to_authorize(self, m_state, m_nonce, m_build):
        m_state.return_value = "STATE123"
        m_nonce.return_value = "NONCE123"
        m_build.return_value = "https://oidc.example/authorize?x=y"

        resp = self.client_api.get("/api/auth/oidc/login")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], "https://oidc.example/authorize?x=y")

        session = self.client_api.session
        self.assertEqual(session.get("oidc_state"), "STATE123")
        self.assertEqual(session.get("oidc_nonce"), "NONCE123")
        self.assertTrue(session.get("oidc_state_ts") is not None)

    # CALLBACK - ERROR
    def test_callback_returns_400_on_oidc_error(self):
        resp = self.client_api.get(
            "/api/auth/oidc/callback?error=login_required&error_description=The%20request%20requires%20login.&state=x"
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("detail", resp.json())

    # CALLBACK - SUCCESS
    @patch("auth_oidc.views.mark_app_user_login")
    @patch("auth_oidc.views.get_active_app_user_by_nni")
    @patch("auth_oidc.oidc_service.GardianOIDCService.validate_id_token")
    @patch("auth_oidc.oidc_service.requests.post")
    def test_callback_success_sets_session_user_and_tokens(
        self, m_post, m_validate_id_token, m_get_user, m_mark_login
    ):
        # Mock user applicatif
        fake_user = MagicMock()
        fake_user.id = 1
        fake_user.nni = "testuser"
        fake_user.role = "READ_ONLY"
        fake_user.is_active = True
        m_get_user.return_value = fake_user
        m_mark_login.return_value = fake_user

        self._set_session(self.client_api, {
            "oidc_state": "STATE_OK",
            "oidc_state_ts": int(time.time()),
            "oidc_nonce": "NONCE_OK",
        })

        m_validate_id_token.return_value = {
            "sub": "abc",
            "nonce": "NONCE_OK",
        }

        token_response = Mock()
        token_response.status_code = 200
        token_response.json.return_value = {
            "access_token": "ACCESS123",
            "refresh_token": "REFRESH123",
            "id_token": "dummy.id.token",
            "expires_in": 3600,
            "scope": "openid name mail",
            "token_type": "Bearer",
        }

        userinfo_response = Mock()
        userinfo_response.status_code = 200
        userinfo_response.json.return_value = {
            "sub": "abc",
            "uid": "testuser",
            "name": "usertest",
            "mail": "user.test@example.com",
        }

        m_post.side_effect = [token_response, userinfo_response]

        resp = self.client_api.get("/api/auth/oidc/callback?code=CODE123&state=STATE_OK")
        self.assertEqual(resp.status_code, 302)

        session = self.client_api.session
        self.assertEqual(session["user"]["sub"], "abc")
        self.assertEqual(session["user"]["name"], "usertest")
        self.assertEqual(session.get("oidc_access_token"), "ACCESS123")
        self.assertEqual(session.get("oidc_refresh_token"), "REFRESH123")
        self.assertEqual(session.get("oidc_id_token"), "dummy.id.token")
        self.assertIsNone(session.get("oidc_state"))

    # ME
    def test_me_returns_401_if_not_authenticated(self):
        resp = self.client_api.get("/api/auth/me")
        self.assertEqual(resp.status_code, 401)

    def test_me_returns_200_if_authenticated(self):
        self._set_session(self.client_api, {
            "user": {"sub": "x", "name": "A", "mail": "a@b", "nni": "testuser"}
        })
        resp = self.client_api.get("/api/auth/me")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["authenticated"])
        self.assertEqual(data["user"]["sub"], "x")

    # REFRESH
    @patch("auth_oidc.oidc_service.requests.post")
    def test_refresh_401_if_no_refresh_token(self, m_post):
        self._set_session(self.client_api, {
            "user": {"sub": "x", "nni": "testuser"}
        })
        resp = self.client_api.post("/api/auth/oidc/refresh")
        self.assertEqual(resp.status_code, 401)

    @patch("auth_oidc.oidc_service.requests.post")
    def test_refresh_success_updates_access_token(self, m_post):
        self._set_session(self.client_api, {
            "user": {"sub": "x", "nni": "testuser"},
            "oidc_refresh_token": "REFRESH_OLD",
            "oidc_access_token": "ACCESS_OLD",
        })

        refresh_response = Mock()
        refresh_response.status_code = 200
        refresh_response.json.return_value = {
            "access_token": "ACCESS_NEW",
            "expires_in": 3600,
            "scope": "openid name mail",
            "token_type": "Bearer",
            "id_token": "IDTOKEN_NEW",
        }

        userinfo_response = Mock()
        userinfo_response.status_code = 200
        userinfo_response.json.return_value = {"sub": "x", "name": "Youssef", "mail": "y@b"}

        m_post.side_effect = [refresh_response, userinfo_response]

        resp = self.client_api.post("/api/auth/oidc/refresh")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["ok"], True)

        session = self.client_api.session
        self.assertEqual(session.get("oidc_access_token"), "ACCESS_NEW")
        self.assertEqual(session.get("oidc_id_token"), "IDTOKEN_NEW")
        self.assertEqual(session.get("user")["name"], "Youssef")


class OIDCLogoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        s = self.client.session
        s["oidc_id_token"] = "IDTOKEN123"
        s.save()

    @patch("auth_oidc.views.GardianOIDCService")
    def test_logout_get_redirects_to_guardian_end_session(self, MockService):
        svc = MockService.return_value
        svc.cfg.endsession_url = "https://oidc.example/endSession"
        svc.post_logout_redirect_uri = "https://app.example/logged-out"

        resp = self.client.get("/api/auth/oidc/logout", follow=False)

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp["Location"].startswith("https://oidc.example/endSession?"))
        self.assertIn("id_token_hint=IDTOKEN123", resp["Location"])
        self.assertIn("post_logout_redirect_uri=", resp["Location"])
