import { Component, Input, OnInit, inject } from '@angular/core';
import { RouterLink, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../core/services/auth.service';
import { User } from '../../../models/user.model';

export interface BreadcrumbItem {
  label: string;
  route?: string;
}

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent implements OnInit {
  @Input() breadcrumbs: BreadcrumbItem[] = [];

  private authService = inject(AuthService);
  private router = inject(Router);

  currentUser: User | null = null;
  showUserMenu = false;

  ngOnInit(): void {
    this.authService.currentUser$.subscribe((user) => {
      this.currentUser = user;
    });
  }

  get fullName(): string {
    return this.authService.fullName;
  }

  get userInitials(): string {
    return this.authService.userInitials;
  }

  get userRole(): string {
    return this.authService.userRole;
  }

  toggleUserMenu(): void {
    this.showUserMenu = !this.showUserMenu;
  }

  closeUserMenu(): void {
    this.showUserMenu = false;
  }

  onLogout(): void {
  this.authService.logout();
}
//   onLogout(): void {
//     this.authService.logout().subscribe({
//       next: () => {
//         this.currentUser = null;
//         this.router.navigate(['/non-connecte']);
//       },
//       error: () => {
//         this.router.navigate(['/non-connecte']);
//       },
//     });
//   }
}