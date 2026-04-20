import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AuthResponse, User } from '../../models/user.model';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {}

  getMe(): Observable<AuthResponse> {
    return this.http.get<AuthResponse>(`${environment.apiBaseUrl}/auth/me`, {
      withCredentials: true,
    }).pipe(
      tap((response) => {
        if (response.authenticated && response.authorized !== false) {
          this.currentUserSubject.next(response.user ?? null);
        } else {
          this.currentUserSubject.next(null);
        }
      })
    );
  }

  logout(): void {
    window.location.href = `${environment.apiBaseUrl}/auth/oidc/logout`;
  }

  get currentUser(): User | null {
    return this.currentUserSubject.getValue();
  }

  get fullName(): string {
    return this.currentUser?.name || '';
  }

  get userInitials(): string {
    const user = this.currentUser;
    if (!user) return '?';
    const parts = user.name.trim().split(' ');
    if (parts.length >= 2) {
      return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase();
    }
    return parts[0][0].toUpperCase();
  }

  get userRole(): string {
    return this.currentUser?.role || '';
  }

  get isAdmin(): boolean {
    return this.currentUser?.role === 'ADMIN';
  }
}