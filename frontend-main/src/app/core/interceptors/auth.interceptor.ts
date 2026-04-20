import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { Router } from '@angular/router';
import { ToastService } from '../services/toast.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const toastService = inject(ToastService);
  const router = inject(Router);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      const detail = error.error?.detail
        || error.error?.message
        || error.error?.error
        || null;

      const code = error.error?.code || null;

      // 403 : utilisateur non déclaré dans la base applicative
      if (error.status === 403) {
        router.navigate(['/non-connecte'], {
          state: {
            reason: code || 'APP_USER_NOT_FOUND',
            detail: detail || 'Accès refusé.'
          },
          replaceUrl: true,
        });
        return throwError(() => error);
      }

      // ── 401 : session expirée ──
      if (error.status === 401) {
        router.navigate(['/non-connecte'], {
          replaceUrl: true,
        });
        return throwError(() => error);
      }

      // ── Autres erreurs → toast ──
      let message = 'Une erreur est survenue.';

      switch (error.status) {
        case 400:
          message = detail || 'Données invalides.';
          break;
        case 404:
          message = detail || 'Ressource introuvable.';
          break;
        case 405:
          message = detail || 'Méthode non autorisée.';
          break;
        case 409:
          message = detail || 'Conflit — cet élément existe déjà.';
          break;
        case 422:
          message = detail || 'Données incorrectes.';
          break;
        case 500:
          message = detail || 'Erreur serveur. Veuillez réessayer plus tard.';
          break;
        case 0:
          message = 'Impossible de contacter le serveur.';
          break;
        default:
          message = detail || `Erreur ${error.status}.`;
      }

      toastService.error(message);
      return throwError(() => error);
    })
  );
};