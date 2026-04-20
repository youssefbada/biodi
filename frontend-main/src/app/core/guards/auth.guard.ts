// import { inject } from '@angular/core';
// import { CanActivateFn, Router } from '@angular/router';
// import { AuthService } from '../services/auth.service';
// import { map, catchError, of } from 'rxjs';

// export const authGuard: CanActivateFn = () => {
//   const authService = inject(AuthService);
//   const router = inject(Router);

//   return authService.getMe().pipe(
//     map((response) => {
//       if (response.authenticated) {
//         return true;
//       }
//       router.navigate(['/non-connecte']);
//       return false;
//     }),
//     catchError(() => {
//       router.navigate(['/non-connecte']);
//       return of(false);
//     })
//   );
// };
// import { inject } from '@angular/core';
// import { CanActivateFn, Router } from '@angular/router';
// import { AuthService } from '../services/auth.service';
// import { map, catchError, of } from 'rxjs';

// export const authGuard: CanActivateFn = () => {
//   const authService = inject(AuthService);
//   const router = inject(Router);

//   return authService.getMe().pipe(
//     map((response) => {
//       if (response.authenticated) return true;
//       router.navigate(['/non-connecte']);
//       return false;
//     }),
//     catchError(() => {
//       router.navigate(['/non-connecte']);
//       return of(false);
//     })
//   );
// };



import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { map, catchError, of } from 'rxjs';
import { environment } from '../../../environments/environment';

export const authGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  return authService.getMe().pipe(
    map((response) => {
      // Pas authentifié du tout
      if (!response.authenticated) {
        router.navigate(['/non-connecte']);
        return false;
      }

      // Authentifié mais pas autorisé (pas dans la base applicative)
      if (response.authorized === false) {
        router.navigate(['/non-connecte'], {
          state: { reason: response.code || 'access_denied' }
        });
        return false;
      }

      return true;
    }),
    catchError(() => {
      if (!environment.production) {
        console.warn('Auth guard: pas de session, mode dev local');
        return of(true);
      }
      router.navigate(['/non-connecte']);
      return of(false);
    })
  );
};