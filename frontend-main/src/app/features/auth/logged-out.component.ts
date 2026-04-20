import { Component, OnInit } from '@angular/core';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-logged-out',
  standalone: true,
  template: `<div></div>`,
})
export class LoggedOutComponent implements OnInit {
  ngOnInit(): void {
    window.location.href = `${environment.apiBaseUrl}/auth/oidc/login`;
  }
}