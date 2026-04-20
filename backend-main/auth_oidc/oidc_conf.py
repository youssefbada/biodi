from dataclasses import dataclass
from django.conf import settings

@dataclass(frozen=True)
class OIDCConfig:
    base_url: str
    client_id: str
    client_secret: str
    redirect_uri: str
    post_logout_redirect_uri: str
    allowed_id_token_algs: list
    scope: str
    acr_values: str | None

    state_ttl_seconds: int
    session_fallback_ttl_seconds: int
    grant_type: str

    @property
    def authorize_url(self) -> str:
        return f"{self.base_url}/gardianwebsso/oauth2/multiauth/authorize"

    @property
    def token_url(self) -> str:
        return f"{self.base_url}/gardianwebsso/oauth2/multiauth/access_token"

    @property
    def userinfo_url(self) -> str:
        return f"{self.base_url}/gardianwebsso/oauth2/multiauth/userinfo"

    @property
    def endsession_url(self) -> str:
        return f"{self.base_url}/gardianwebsso/oauth2/multiauth/connect/endSession"

    @property
    def gardian_jwk_url(self) -> str:
        return f"{self.base_url}/gardianwebsso/oauth2/multiauth/connect/jwk_uri"

    @property
    def gardian_issuer(self) -> str:
        return f"{self.base_url}:443/gardianwebsso/oauth2/multiauth"


def get_oidc_config() -> OIDCConfig:
    cfg = settings.OIDC_GARDIAN

    base_url = (cfg.get("BASE_URL") or "").rstrip("/")
    if not base_url:
        raise RuntimeError("Missing settings.OIDC_GARDIAN['BASE_URL']")

    return OIDCConfig(
        base_url=base_url,
        client_id=cfg["CLIENT_ID"],
        client_secret=cfg["CLIENT_SECRET"],
        redirect_uri=cfg["REDIRECT_URI"],
        post_logout_redirect_uri=cfg["POST_LOGOUT_REDIRECT_URI"],
        scope=cfg.get("SCOPE", "openid"),
        acr_values=cfg.get("ACR_VALUES"),
        allowed_id_token_algs=cfg["ALLOWED_ID_TOKEN_ALGS"],
        state_ttl_seconds=int(cfg.get("STATE_TTL_SECONDS", 300)),
        session_fallback_ttl_seconds=int(cfg.get("SESSION_FALLBACK_TTL_SECONDS", 3600)),
        grant_type=cfg.get("grant_type", "authorization_code"),

    )
