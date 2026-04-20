import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

interface NavItem {
  label: string;
  icon: string;
  route: string;
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss',
})
export class SidebarComponent {
  navItems: NavItem[] = [
    { label: 'Accueil',         icon: 'home',            route: '/accueil'                },
    { label: 'Centrales',       icon: 'centrales',       route: '/centrales'       },
    { label: 'Poissons',        icon: 'poissons',        route: '/poissons'        },
    { label: 'Non-poissons',    icon: 'non-poissons',    route: '/non-poissons'    },
    { label: 'Échantillonnage', icon: 'echantillonnage', route: '/echantillonnage' },
    { label: 'Inventaire',      icon: 'inventaire',      route: '/inventaire'      },
    { label: 'Requêtes',        icon: 'requetes',        route: '/requetes'        },
    { label: 'Utilisateurs',    icon: 'utilisateurs',    route: '/utilisateurs'    },
  ];
}