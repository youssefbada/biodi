from django.urls import path
from auth_oidc.views import OIDCLoginView, OIDCCallbackView, LogoutView, MeView, OIDCRefreshView

urlpatterns = [
    path("oidc/login", OIDCLoginView.as_view(), name="oidc_login"),
    path("oidc/callback", OIDCCallbackView.as_view(), name="oidc_callback"),
    path("oidc/logout", LogoutView.as_view(), name="oidc_logout"),
    path("oidc/refresh", OIDCRefreshView.as_view(), name="oidc_refresh"),
    path("me", MeView.as_view(), name="me"),
]
