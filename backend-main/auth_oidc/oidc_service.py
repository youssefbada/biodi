import os
import time
import secrets
import requests
import jwt
from jwt import PyJWKClient
import logging
from urllib.parse import urlencode

from auth_oidc.exceptions import OIDCStateError, OIDCTokenError, OIDCUserinfoError
from auth_oidc.dto.user_dto import OIDCUserDTO
from auth_oidc.oidc_conf import get_oidc_config
logger = logging.getLogger(__name__)

class GardianOIDCService:
    """
    Service d’intégration OIDC Gardian (code flow).
    - Construit l’URL authorize
    - Echange code -> tokens
    - Appelle userinfo
    """
    def __init__(self):

        self.cfg = get_oidc_config()

        if not self.cfg.client_id or not self.cfg.client_secret:
            raise RuntimeError("Missing OIDC client credentials (CLIENT_ID / CLIENT_SECRET)")
        if not self.cfg.redirect_uri:
            raise RuntimeError("Missing OIDC redirect_uri")
        if not self.cfg.post_logout_redirect_uri:
            raise RuntimeError("Missing post_logout_redirect_uri")

    def generate_state(self) -> str:
        return secrets.token_urlsafe(32)

    def generate_nonce(self) -> str:
        return secrets.token_urlsafe(32)

    def build_authorize_url(self, state: str, nonce: str) -> str:
        params = {
            "response_type": "code",
            "client_id": self.cfg.client_id,
            "scope": self.cfg.scope,
            "redirect_uri": self.cfg.redirect_uri,
            "state": state,
            "nonce": nonce,
            "acr_values": self.cfg.acr_values
        }

        query = urlencode(params, safe="%")

        logger.info(
            "OIDC authorize URL generated (client_id=%s, redirect_uri=%s, scope=%s)",
            self.cfg.client_id, self.cfg.redirect_uri, self.cfg.scope
        )

        url = f"{self.cfg.authorize_url}?{query}"
        logger.debug("OIDC authorize full URL=%s", url)
        return url

    def validate_state(self, request_state: str, expected_state: str, ts: int):
        if not expected_state or request_state != expected_state:
            logger.warning("OIDC state invalid (expected_present=%s)", bool(expected_state))
            raise OIDCStateError("Invalid state")

        age = int(time.time()) - int(ts or 0)
        if age > self.cfg.state_ttl_seconds:
            logger.warning("OIDC state expired (age=%s ttl=%s)", age, self.cfg.state_ttl_seconds)
            raise OIDCStateError("State expired")

        logger.debug("OIDC state validated (age_seconds=%s)", age)

    def clear_oidc_flow_session(self, request) -> None:
        """
        Nettoie uniquement les clés temporaires du flow OIDC (state/nonce/ts).
        Ne touche pas à la session user.
        """
        for k in ["oidc_state", "oidc_nonce", "oidc_state_ts"]:
            request.session.pop(k, None)

    def clear_oidc_tokens_session(self, request) -> None:
        for k in ["oidc_access_token", "oidc_refresh_token", "oidc_id_token", "oidc_scope", "oidc_expires_in"]:
            request.session.pop(k, None)

    def should_retry_login(self, request, max_retry: int = 1) -> bool:
        """
        Anti-boucle: autorise max_retry relance(s) auto.
        """
        retry = int(request.session.get("oidc_retry", 0)) + 1
        request.session["oidc_retry"] = retry
        return retry <= max_retry

    def clear_retry(self, request) -> None:
        request.session.pop("oidc_retry", None)

    def validate_id_token(self, id_token:str, nonce_expected:str) -> dict:
        if not id_token:
            raise OIDCTokenError("Missing id_token")

        jwk_client = PyJWKClient(self.cfg.gardian_jwk_url)

        signing_key = jwk_client.get_signing_key_from_jwt(id_token)

        claims = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=self.cfg.allowed_id_token_algs,
            audience=self.cfg.client_id,
            issuer=self.cfg.gardian_issuer,
            options={
                "require": ["exp", "iat"]
            },
        )
        token_nonce = claims.get("nonce")

        if nonce_expected and token_nonce != nonce_expected:
            raise OIDCTokenError("Invalid nonce in id_token")
        logger.info(claims)
        return claims

    def exchange_code_for_token(self, code: str) -> dict:
        start = time.time()
        logger.info("OIDC token exchange started (grant_type=authorization_code)")
        logger.info(code)
        resp = requests.post(
            self.cfg.token_url,
            data={
                "grant_type": self.cfg.grant_type,
                "code": code,
                "redirect_uri": self.cfg.redirect_uri,
            },
            auth=(self.cfg.client_id, self.cfg.client_secret),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )
        duration_ms = int((time.time() - start) * 1000)
        if resp.status_code != 200:
            logger.error(
                "OIDC token exchange failed (status=%s, duration_ms=%s, body=%s)",
                resp.status_code, duration_ms, resp.text[:300]
            )
            raise OIDCTokenError(f"Token exchange failed: {resp.status_code} {resp.text}")

        #TODO à supprmier
        logger.info(
            "OIDC token exchange success (duration_ms=%s, has_access_token=%s, has_refresh_token=%s, has_id_token=%s)",
            duration_ms,
            bool(resp.json().get("access_token")),
            bool(resp.json().get("refresh_token")),
            bool(resp.json().get("id_token")),
        )
        return resp.json()

    def fetch_userinfo(self, access_token: str) -> dict:
        resp = requests.post(
            self.cfg.userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        if resp.status_code != 200:
            raise OIDCUserinfoError(f"Userinfo failed: {resp.status_code} {resp.text}")
        logger.info(resp.json())
        return resp.json()

    def refresh_access_token(self, refresh_token: str) -> dict:
        """
        Refresh token flow (grant_type=refresh_token)
        Doc Gardian:
          - POST access_token
          - body: grant_type=refresh_token & refresh_token=...
          - auth: Basic (client_id/client_secret)
        """
        if not refresh_token:
            raise OIDCTokenError("Missing refresh_token")

        resp = requests.post(
            self.cfg.token_url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            auth=(self.cfg.client_id, self.cfg.client_secret),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )

        if resp.status_code != 200:
            raise OIDCTokenError(f"Refresh token failed: {resp.status_code} {resp.text}")

        return resp.json()

    def authenticate_from_callback(self, request) -> OIDCUserDTO:
        """
        Utilisé par la vue callback.
        Vérifie code/state, échange token, récupère userinfo, retourne DTO.
        """
        if request.GET.get("error"):
            err = request.GET.get("error")
            desc = request.GET.get("error_description", "")
            logger.warning("OIDC callback returned error (error=%s, desc=%s)", err, desc)
            raise OIDCUserinfoError(
                f"OIDC error={request.GET.get('error')} desc={request.GET.get('error_description','')}"
            )

        code = request.GET.get("code")
        state = request.GET.get("state")
        if not code or not state:
            raise OIDCStateError("Missing code/state")

        expected_state = request.session.get("oidc_state")
        nonce_expected = request.session.get("oidc_nonce")
        ts = request.session.get("oidc_state_ts", 0)
        logger.info(state)
        logger.info(expected_state)
        logger.info(ts)
        self.validate_state(state, expected_state, ts)

        token_data = self.exchange_code_for_token(code)
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        id_token = token_data.get("id_token")

        self.validate_id_token(id_token=id_token, nonce_expected=nonce_expected)

        if not access_token:
            raise OIDCTokenError("No access_token returned")

        request.session["oidc_access_token"] = access_token
        request.session["oidc_refresh_token"] = refresh_token
        request.session["oidc_id_token"] = id_token
        request.session["oidc_scope"] = token_data.get("scope")

        expires_in_raw = token_data.get("expires_in")
        try:
            expires_in = int(expires_in_raw or 0)
        except (TypeError, ValueError):
            expires_in = 0

        ttl = expires_in if expires_in > 0 else self.cfg.session_fallback_ttl_seconds
        request.session["oidc_expires_in"] = expires_in
        request.session["oidc_expires_at"] = int(time.time()) + ttl
        request.session.set_expiry(ttl)

        logger.info(
            "OIDC tokens stored (has_refresh=%s, has_id_token=%s, expires_in=%s, ttl_used=%s)",
            bool(refresh_token),
            bool(id_token),
            expires_in,
            ttl,
        )

        userinfo = self.fetch_userinfo(access_token)
        return OIDCUserDTO.from_userinfo(userinfo)
