// import { Component, OnInit } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { AuthService } from '../../core/services/auth.service';
// import { OidcUser } from '../../core/models/user.model';

// @Component({
//   selector: 'app-home',
//   standalone: true,
//   imports: [CommonModule],
//   templateUrl: './home.component.html',
// })
// export class HomeComponent implements OnInit {
//   loading = true;
//   user?: OidcUser;
//   error?: string;

//   constructor(private readonly auth: AuthService) {}

//   ngOnInit(): void {
//     this.auth.me().subscribe({
//       next: (res) => {
//         console.log(this.loading,"hdhdhhdhdhdhhd")

//         this.loading = false;
//         if (!res.authenticated) {
//           // // théoriquement guard empêche ça, mais au cas où
//           // this.auth.redirectToLogin('/');
//           // return;
//         }
//         this.user = res.user;
//         console.log(this.user,"hdhdhhdhdhdhhd")
//       },
//       error: (e) => {
//         this.loading = false;
//         this.error = 'Erreur appel /me';
//         console.error(e);
//       }
//     });
//   }

//   logout() {
//     // 1) logout appli (flush session django)
//     this.auth.logoutAppSession().subscribe({
//       next: () => {
//         // 2) logout Gardian (endSession) via backend
//         this.auth.redirectToGardianLogout();
//       },
//       error: (e) => {
//         console.error(e);
//         // fallback : au moins tenter la redirection logout sso
//         this.auth.redirectToGardianLogout();
//       }
//     });
//   }
// }
