import { Component, OnInit, inject } from '@angular/core';
import { RouterOutlet, Router, ActivatedRoute } from '@angular/router';
import { ToastComponent } from './shared/components/toast/toast.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ToastComponent],
  templateUrl: './app.html',
})
export class App implements OnInit {
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  ngOnInit(): void {
    const params = new URLSearchParams(window.location.search);
    const sso = params.get('sso');
    const reason = params.get('reason');

    if (sso === 'ko' && reason === 'access_denied') {
      this.router.navigate(['/non-connecte'], {
        state: { reason: 'APP_USER_NOT_FOUND' },
        replaceUrl: true,
      });
      return;
    }
  }
}