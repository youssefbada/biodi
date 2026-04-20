from functools import wraps
from django.http import JsonResponse
from rest_framework import status

from core.services.app_user_access_service import get_active_app_user_by_nni
from core.exceptions.api_exceptions import ApiException

def _resolve_session_app_user(request):
  """
  Résout l'utilisateur applicatif à partir de la session.
  Vérifie :
  - session présente
  - pas d'erreur auth stockée
  - nni présent
  - utilisateur présent en base
  - utilisateur actif
  """

  user = request.session.get("user")
  auth_error = request.session.get("auth_error")

  # pas de session
  if not user:
    return None, None, JsonResponse(
      {
        "authenticated": False,
        "authorized": False,
        "detail": "Not authenticated",
      },
      status=status.HTTP_401_UNAUTHORIZED,
    )

  # session OIDC OK mais accès applicatif refusé
  if auth_error:
    return None, None, JsonResponse(
      {
        "authenticated": True,
        "authorized": False,
        "reason": auth_error.get("reason"),
        "code": auth_error.get("code"),
        "detail": auth_error.get("detail"),
      },
      status=status.HTTP_403_FORBIDDEN,
    )

  nni = user.get("nni")

  if not nni:
    return None, None, JsonResponse(
      {
        "authenticated": True,
        "authorized": False,
        "detail": "Missing NNI in session",
      },
      status=status.HTTP_403_FORBIDDEN,
    )

  try:
    app_user = get_active_app_user_by_nni(nni)

  except ApiException as e:
    return None, None, JsonResponse(
      {
        "authenticated": True,
        "authorized": False,
        "code": e.code,
        "detail": e.detail,
      },
      status=status.HTTP_403_FORBIDDEN,
    )

  return user, app_user, None

def require_session_user(view_func):
  """
  Vérifie que l'utilisateur est :
  - authentifié via session
  - autorisé dans l'application
  """

  @wraps(view_func)
  def _wrapped(request, *args, **kwargs):

    user, app_user, error_response = _resolve_session_app_user(request)

    if error_response:
      return error_response

    # exposer user dans la request
    request.oidc_user = user
    request.app_user = app_user

    return view_func(request, *args, **kwargs)

  return _wrapped

def require_admin_user(view_func):
  """
  Vérifie :
  - utilisateur connecté
  - utilisateur autorisé
  - rôle ADMIN
  """

  @wraps(view_func)
  def _wrapped(request, *args, **kwargs):

    user, app_user, error_response = _resolve_session_app_user(request)

    if error_response:
      return error_response

    if app_user.role != "ADMIN":
      return JsonResponse(
        {
          "authenticated": True,
          "authorized": False,
          "detail": "Access denied: admin role required",
        },
        status=status.HTTP_403_FORBIDDEN,
      )

    request.oidc_user = user
    request.app_user = app_user

    return view_func(request, *args, **kwargs)

  return _wrapped
