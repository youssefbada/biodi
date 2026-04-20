import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { confirmLeaveGuard } from './core/guards/confirm-leave.guard';

export const routes: Routes = [

//   {
//   path: 'accueil',
//   canActivate: [authGuard],
//   loadComponent: () =>
//     import('./features/dashboard/dashboard.component').then(
//       (m) => m.DashboardComponent
//     ),
// },
  {
    path: '',
    redirectTo: 'centrales',
    pathMatch: 'full',
  },
  {
  path: 'logged-out',
  loadComponent: () =>
    import('./features/auth/logged-out.component').then(
      (m) => m.LoggedOutComponent
    ),
},
  {
    path: 'non-connecte',
    loadComponent: () =>
      import('./features/auth/unauthorized.component').then(
        (m) => m.UnauthorizedComponent
      ),
  },
  {
    path: 'centrales',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/centrales/centrales-list/centrales-list.component').then(
        (m) => m.CentralesListComponent
      ),
  },
  {
    path: 'centrales/nouveau',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/centrales/centrales-form/centrales-form.component').then(
        (m) => m.CentralesFormComponent
      ),
  },
  {
    path: 'centrales/:id/modifier',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/centrales/centrales-form/centrales-form.component').then(
        (m) => m.CentralesFormComponent
      ),
  },
  {
    path: 'centrales/:id',
    canActivate: [authGuard],
    canDeactivate: [confirmLeaveGuard],
    loadComponent: () =>
      import('./features/centrales/centrales-detail/centrales-detail.component').then(
        (m) => m.CentralesDetailComponent
      ),
  },
{
  path: 'poissons',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./features/poissons/poissons-list/poissons-list.component').then(
      (m) => m.PoissonsListComponent
    ),
},
{
  path: 'poissons/nouveau',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./features/poissons/poissons-form/poissons-form.component').then(
      (m) => m.PoissonsFormComponent
    ),
},
{
  path: 'poissons/:id/modifier',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./features/poissons/poissons-form/poissons-form.component').then(
      (m) => m.PoissonsFormComponent
    ),
},
{
  path: 'poissons/:id',
  canActivate: [authGuard],
  canDeactivate: [confirmLeaveGuard],
  loadComponent: () =>
    import('./features/poissons/poissons-detail/poissons-detail.component').then(
      (m) => m.PoissonsDetailComponent
    ),
},

{
  path: 'non-poissons',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./features/non-poissons/non-poissons-list/non-poissons-list.component').then(
      (m) => m.NonPoissonsListComponent
    ),
},
{
  path: 'non-poissons/nouveau',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./features/non-poissons/non-poissons-form/non-poissons-form.component').then(
      (m) => m.NonPoissonsFormComponent
    ),
},
{
  path: 'non-poissons/:id/modifier',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./features/non-poissons/non-poissons-form/non-poissons-form.component').then(
      (m) => m.NonPoissonsFormComponent
    ),
},
{
  path: 'non-poissons/:id',
  canActivate: [authGuard],
  canDeactivate: [confirmLeaveGuard],
  loadComponent: () =>
    import('./features/non-poissons/non-poissons-detail/non-poissons-detail.component').then(
      (m) => m.NonPoissonsDetailComponent
    ),
},

// {
//   path: 'echantillonnage',
//   canActivate: [authGuard],
//   loadComponent: () =>
//     import('./features/echantillonnage/echantillonnage-list/echantillonnage-list.component').then(
//       (m) => m.EchantillonnageListComponent
//     ),
// },
// {
//   path: 'echantillonnage/nouveau',
//   canActivate: [authGuard],
//   loadComponent: () =>
//     import('./features/echantillonnage/echantillonnage-form/echantillonnage-form.component').then(
//       (m) => m.EchantillonnageFormComponent
//     ),
// },
// {
//   path: 'echantillonnage/:id/modifier',
//   canActivate: [authGuard],
//   loadComponent: () =>
//     import('./features/echantillonnage/echantillonnage-form/echantillonnage-form.component').then(
//       (m) => m.EchantillonnageFormComponent
//     ),
// },
// {
//   path: 'echantillonnage/:id',
//   canActivate: [authGuard],
//   canDeactivate: [confirmLeaveGuard],
//   loadComponent: () =>
//     import('./features/echantillonnage/echantillonnage-detail/echantillonnage-detail.component').then(
//       (m) => m.EchantillonnageDetailComponent
//     ),
// },

// {
//   path: 'inventaire',
//   canActivate: [authGuard],
//   loadComponent: () =>
//     import('./features/inventaire/inventaire-list/inventaire-list.component').then(
//       (m) => m.InventaireListComponent
//     ),
// },
// {
//   path: 'inventaire/nouveau',
//   canActivate: [authGuard],
//   loadComponent: () =>
//     import('./features/inventaire/inventaire-form/inventaire-form.component').then(
//       (m) => m.InventaireFormComponent
//     ),
// },
// {
//   path: 'inventaire/:id/modifier',
//   canActivate: [authGuard],
//   loadComponent: () =>
//     import('./features/inventaire/inventaire-form/inventaire-form.component').then(
//       (m) => m.InventaireFormComponent
//     ),
// },
// {
//   path: 'inventaire/:id',
//   canActivate: [authGuard],
//   canDeactivate: [confirmLeaveGuard],
//   loadComponent: () =>
//     import('./features/inventaire/inventaire-detail/inventaire-detail.component').then(
//       (m) => m.InventaireDetailComponent
//     ),
// },


  {
    path: '**',
    redirectTo: 'centrales',
  },
];