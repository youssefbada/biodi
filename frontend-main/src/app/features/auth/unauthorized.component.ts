import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-unauthorized',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="unauth-page">
      <div class="unauth-card">
        <div class="unauth-icon">
          <span class="material-symbols-outlined">
            {{ isAppUserNotFound ? 'person_off' : 'lock' }}
          </span>
        </div>

        @if (isAppUserNotFound) {
          <h1 class="unauth-title">Accès refusé</h1>
          <p class="unauth-message">
            Votre compte n'est pas déclaré dans l'application Biodiv.<br/>
            Veuillez contacter votre administrateur pour obtenir un accès.
          </p>
          <button class="unauth-btn unauth-btn--secondary" (click)="onSwitchAccount()">
            <span class="material-symbols-outlined">switch_account</span>
            Se connecter avec un autre compte
          </button>
        } @else {
          <h1 class="unauth-title">Session expirée</h1>
          <p class="unauth-message">
            Vous n'êtes pas connecté ou votre session a expiré.<br/>
            Veuillez vous reconnecter pour accéder à l'application.
          </p>
          <a [href]="loginUrl" class="unauth-btn">
            <span class="material-symbols-outlined">login</span>
            Se connecter
          </a>
        }
      </div>
    </div>
  `,
  styles: [`
    .unauth-page {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #f6f6f8;
      font-family: 'Inter', sans-serif;
    }

    .unauth-card {
      background: white;
      border-radius: 12px;
      padding: 3rem 2.5rem;
      text-align: center;
      box-shadow: 0 4px 24px rgba(0,0,0,0.08);
      border: 1px solid #e5e7eb;
      max-width: 420px;
      width: 100%;
    }

    .unauth-icon {
      width: 4rem;
      height: 4rem;
      border-radius: 50%;
      background-color: rgba(0,26,112,0.08);
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 1.5rem;

      .material-symbols-outlined {
        font-size: 2rem;
        color: #001A70;
      }
    }

    .unauth-title {
      font-size: 1.5rem;
      font-weight: 700;
      color: #111318;
      margin: 0 0 0.75rem;
    }

    .unauth-message {
      font-size: 0.9rem;
      color: #616f89;
      line-height: 1.6;
      margin: 0 0 2rem;
    }

    .unauth-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.75rem 2rem;
      background-color: #001A70;
      color: white;
      border-radius: 8px;
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 600;
      border: none;
      cursor: pointer;
      transition: background-color 0.15s;

      &:hover { background-color: #001055; }

      .material-symbols-outlined { font-size: 1.2rem; }

    .unauth-btn--secondary {
      background-color: transparent;
      border: 2px solid #001A70;
      color: #001A70;
      &:hover { background-color: rgba(0,26,112,0.06); }
      }
    }
  `]
})
export class UnauthorizedComponent {
  private authService = inject(AuthService);
  loginUrl = `${environment.apiBaseUrl}/auth/oidc/login`;

  get isAppUserNotFound(): boolean {
    return history.state?.reason === 'APP_USER_NOT_FOUND';
  }

  onSwitchAccount(): void {
    // Déconnecte Gardian → Gardian redirige vers post_logout_redirect_uri
    this.authService.logout();
  }
}