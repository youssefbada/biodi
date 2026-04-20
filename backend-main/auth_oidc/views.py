import time
import logging
from auth_oidc.dto.user_dto import OIDCUserDTO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from auth_oidc.oidc_service import GardianOIDCService
from auth_oidc.exceptions import OIDCStateError, OIDCTokenError, OIDCUserinfoError
from auth_oidc.decorators import require_session_user
from core.services.app_user_access_service import get_active_app_user_by_nni, mark_app_user_login
from core.exceptions.api_exceptions import ApiException
from config.settings import APP_FRONT_URL
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class OIDCLoginView(APIView):
    def get(self, request):
        svc = GardianOIDCService()
        svc.clear_retry(request)

        state = svc.generate_state()
        nonce = svc.generate_nonce()
        request.session["oidc_state"] = state
        request.session["oidc_nonce"] = nonce
        request.session["oidc_state_ts"] = int(time.time())
        logger.warning("OIDC login initiated (session_key=%s)", request.session.session_key)
        url = svc.build_authorize_url(state=state, nonce=nonce)
        logger.info(url)
        return redirect(url)

# class OIDCCallbackView(APIView):
#     def get(self, request):
#         svc = GardianOIDCService()
#         logger.info(request)
#         logger.info("OIDC callback received (has_error=%s, has_code=%s)",
#             bool(request.GET.get("error")), bool(request.GET.get("code"))
#         )
#         try:
#             user_dto = svc.authenticate_from_callback(request)
#         except OIDCStateError as e:
#             logger.warning("OIDC callback state error: %s", str(e))

#             # Nettoie le flow (state/nonce/ts) pour éviter re-jeu
#             svc.clear_oidc_flow_session(request)

#             # Anti-boucle : 1 seule relance auto
#             if svc.should_retry_login(request, max_retry=1):
#                 logger.info("OIDC retrying login after invalid/expired state")
#                 return redirect("/api/auth/oidc/login?reason=state")

#             return Response(
#                 {"detail": "Authentication failed (invalid state). Please retry.", "reason": "invalid_state"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         except (OIDCTokenError, OIDCUserinfoError) as e:
#             logger.warning("OIDC callback failed: %s", str(e))

#             svc.clear_oidc_flow_session(request)

#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         # SUCCESS => reset retry counter
#         svc.clear_retry(request)

#         # session applicative
#         request.session["user"] = {
#             "sub": user_dto.sub,
#             "uid": user_dto.uid,
#             "name": user_dto.name,
#             "givenName": user_dto.givenName,
#             "sn": user_dto.sn,
#             "mail": user_dto.mail,
#         }

#         # Nettoyage anti re-jeu
#         svc.clear_oidc_flow_session(request)

#         logger.info("OIDC callback success (user_sub=%s)", user_dto.sub)

#         return redirect(f"{APP_FRONT_URL}/?sso=ok")



class OIDCCallbackView(APIView):
    def get(self, request):
        svc = GardianOIDCService()

        logger.info(
            "OIDC callback received (has_error=%s, has_code=%s)",
            bool(request.GET.get("error")),
            bool(request.GET.get("code")),
        )

        try:
            user_dto = svc.authenticate_from_callback(request)

        except OIDCStateError as e:
            logger.warning("OIDC callback state error: %s", str(e))

            # Nettoie le flow (state/nonce/ts) pour éviter re-jeu
            svc.clear_oidc_flow_session(request)

            # 1 seule relance auto
            if svc.should_retry_login(request, max_retry=1):
                logger.info("OIDC retrying login after invalid/expired state")
                return redirect("/api/auth/oidc/login?reason=state")

            return Response(
                {
                    "detail": "Authentication failed (invalid state). Please retry.",
                    "reason": "invalid_state",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except (OIDCTokenError, OIDCUserinfoError) as e:
            logger.warning("OIDC callback failed: %s", str(e))

            svc.clear_oidc_flow_session(request)

            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # LIAISON AVEC LA BASE APPLICATIVE
        try:
            app_user = get_active_app_user_by_nni(user_dto.uid)
            app_user = mark_app_user_login(app_user)

        except ApiException as e:
            logger.warning(
                "OIDC callback denied by app user lookup | uid=%s | code=%s | detail=%s",
                user_dto.uid,
                e.code,
                e.detail,
            )

            svc.clear_oidc_flow_session(request)
            # svc.clear_oidc_tokens_session(request)

            request.session["auth_error"] = {
                "reason": "access_denied",
                "code": e.code,
                "detail": e.detail,
                "uid": user_dto.uid,
            }

            request.session["user"] = {
                "uid": user_dto.uid,
                "name": user_dto.name,
                "nni": user_dto.uid,
                # "nni": app_user.nni,
                "givenName": user_dto.givenName,
                "sn": user_dto.sn,
                "mail": user_dto.mail,
                "access_denied": True,
            }

            return redirect(f"{APP_FRONT_URL}/?sso=ko&reason=access_denied")


        # SUCCESS => reset retry counter
        svc.clear_retry(request)

        # session applicative
        request.session["user"] = {
            "id": app_user.id,
            "nni": user_dto.uid,
            "role": app_user.role,
            "is_active": app_user.is_active,

            "sub": user_dto.sub,
            "uid": user_dto.uid,
            "name": user_dto.name,
            "givenName": user_dto.givenName,
            "sn": user_dto.sn,
            "mail": user_dto.mail,
        }

        # Nettoyage anti re-jeu
        svc.clear_oidc_flow_session(request)

        logger.info(
            "OIDC callback success | user_sub=%s | app_user_id=%s | role=%s",
            user_dto.sub,
            app_user.id,
            app_user.role,
        )

        return redirect(f"{APP_FRONT_URL}/?sso=ok")

class LogoutView(APIView):
    def get(self, request):
        """
        Logout complet :
        - flush session Django
        - redirection vers endSession Guardian avec id_token_hint
        """
        svc = GardianOIDCService()

        id_token = request.session.get("oidc_id_token")
        logger.info("Logout requested (has_id_token=%s)", bool(id_token))

        # logout appli
        # Logout appli (nettoyage)
        svc.clear_oidc_flow_session(request)
        svc.clear_oidc_tokens_session(request)
        request.session.pop("user", None)
        request.session.flush()

        if not id_token:
            # pas d'id_token => on ne peut pas faire endSession "propre"
            return redirect(svc.cfg.post_logout_redirect_uri)

        params = {
            "id_token_hint": id_token,
            "post_logout_redirect_uri": svc.cfg.post_logout_redirect_uri,
        }
        end_url = f"{svc.cfg.endsession_url}?{urlencode(params)}"
        logger.info("Logout: redirecting to Gardian endSession")
        logger.info(end_url)
        return redirect(end_url)

    def post(self, request):
        """
        Si tu veux garder un POST pour Postman:
        - logout appli uniquement (pas SSO Guardian)
        """
        request.session.flush()
        return Response({"ok": True, "detail": "App session cleared. Use GET for Guardian SSO logout."}, status=status.HTTP_200_OK)


@method_decorator(require_session_user, name="dispatch")
class MeView(APIView):
    def get(self, request):
        return Response(
           {"authenticated": True, "user": request.oidc_user},
           status=status.HTTP_200_OK
        )

@method_decorator(require_session_user, name="dispatch")
class OIDCRefreshView(APIView):
    """
    Refresh du access_token via refresh_token stocké en session.
    - Met à jour les tokens en session
    - remplace request.session["user"]
    """
    def post(self, request):
        svc = GardianOIDCService()

        refresh_token = request.session.get("oidc_refresh_token")
        if not refresh_token:
            return Response({"detail": "No refresh_token in session"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token_data = svc.refresh_access_token(refresh_token)
        except OIDCTokenError as e:
            logger.warning("OIDC refresh failed: %s", str(e))
            svc.clear_oidc_tokens_session(request)
            request.session.pop("user", None)
            request.session.flush()
            return Response({"detail": "Refresh failed, please login again"}, status=status.HTTP_401_UNAUTHORIZED)

            # si refresh KO alors on invalide la session pour forcer un nouveau login
            request.session.flush()
            return Response({"detail": "Refresh failed, please login again"}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = token_data.get("access_token")
        if not access_token:
            return Response({"detail": "No access_token returned on refresh"}, status=status.HTTP_400_BAD_REQUEST)

        request.session["oidc_access_token"] = access_token
        request.session["oidc_scope"] = token_data.get("scope")
        request.session["oidc_expires_in"] = token_data.get("expires_in")

        if token_data.get("refresh_token"):
            request.session["oidc_refresh_token"] = token_data["refresh_token"]

        if token_data.get("id_token"):
            request.session["oidc_id_token"] = token_data["id_token"]

        try:
            userinfo = svc.fetch_userinfo(access_token)
            user_dto = OIDCUserDTO.from_userinfo(userinfo)
            request.session["user"] = {
                "sub": user_dto.sub,
                "uid": user_dto.uid,
                "name": user_dto.name,
                "givenName": user_dto.givenName,
                "sn": user_dto.sn,
            }
        except Exception as e:
            logger.warning("Userinfo refresh skipped: %s", str(e))

        return Response({"ok": True}, status=status.HTTP_200_OK)
