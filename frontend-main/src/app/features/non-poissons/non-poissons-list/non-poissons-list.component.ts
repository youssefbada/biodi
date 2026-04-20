import { Component, OnInit, OnDestroy, inject, signal, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Subject, debounceTime, distinctUntilChanged, takeUntil } from 'rxjs';

import { NonPoissonsService } from '../../../core/services/non-poissons.service';
import { NonPoisson } from '../../../models/non-poisson.model';
import { AuthService } from '../../../core/services/auth.service';
import { ImportService } from '../../../core/services/import.service';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent, BreadcrumbItem } from '../../../shared/components/header/header.component';
import { ImportModalComponent, ColumnMapping } from '../../../shared/components/import-modal/import-modal.component';
import { ConfirmDeleteModalComponent } from '../../../shared/components/confirm-delete-modal/confirm-delete-modal.component';
import {
  GROUPE_OPTIONS,
  GUILDE_ECOLOGIQUE_OPTIONS,
  REPARTITION_COLONNE_EAU_OPTIONS,
  NON_POISSON_BADGE_COLORS,
} from '../../../core/constants/non-poisson.constants';
import { PAGE_SIZE_DEFAULT } from '../../../core/constants/app.constants';

@Component({
  selector: 'app-non-poissons-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    FormsModule,
    SidebarComponent,
    HeaderComponent,
    ImportModalComponent,
    ConfirmDeleteModalComponent,
  ],
  templateUrl: './non-poissons-list.component.html',
  styleUrl: './non-poissons-list.component.scss',
})
export class NonPoissonsListComponent implements OnInit, OnDestroy {

  private nonPoissonsService = inject(NonPoissonsService);
  private importService = inject(ImportService);
  private cdr = inject(ChangeDetectorRef);
  router = inject(Router);
  authService = inject(AuthService);

  breadcrumbs: BreadcrumbItem[] = [
    { label: 'Accueil', route: '/accueil' },
    { label: 'Non-poissons' },
  ];

  allItems: NonPoisson[] = [];
  itemsFiltres: NonPoisson[] = [];
  totalCount = 0;
  isLoading = false;
  errorMessage = '';

  searchTerm = '';
  selectedGroupe = '';
  selectedGuildeEco = '';
  selectedRepartition = '';

  currentPage = 1;
  pageSize = PAGE_SIZE_DEFAULT;

  groupeOptions = GROUPE_OPTIONS;
  guildeEcoOptions = GUILDE_ECOLOGIQUE_OPTIONS;
  repartitionOptions = REPARTITION_COLONNE_EAU_OPTIONS;
  badgeColors = NON_POISSON_BADGE_COLORS;

  showImportModal = signal(false);
  itemToDelete: NonPoisson | null = null;

  columnMappings: ColumnMapping[] = [
    { excelHeader: 'Groupe',               modelField: 'groupe',               label: 'Groupe',               required: false },
    { excelHeader: 'Famille',              modelField: 'famille',              label: 'Famille',              required: true  },
    { excelHeader: 'Genre',                modelField: 'genre',                label: 'Genre',                required: true  },
    { excelHeader: 'Espèce',               modelField: 'espece',               label: 'Espèce',               required: true  },
    { excelHeader: 'Nom commun',           modelField: 'nom_commun',           label: 'Nom commun',           required: true  },
    { excelHeader: 'Guilde écologique',    modelField: 'guilde_ecologique',    label: 'Guilde écologique',    required: false },
    { excelHeader: 'Répartition colonne eau', modelField: 'repartition_colonne_eau', label: 'Répartition', required: false },
    { excelHeader: 'Guilde trophique',     modelField: 'guilde_trophique',     label: 'Guilde trophique',     required: false },
    { excelHeader: 'Enjeu halieutique',    modelField: 'enjeu_halieutique',    label: 'Enjeu halieutique',    required: false },
    { excelHeader: 'État stock',           modelField: 'etat_stock',           label: 'État stock',           required: false },
    { excelHeader: 'Statut protection',    modelField: 'statut_protection',    label: 'Statut protection',    required: false },
    { excelHeader: 'Conservation FR',      modelField: 'conservation_fr',      label: 'Conservation FR',      required: false },
    { excelHeader: 'Conservation EU',      modelField: 'conservation_eu',      label: 'Conservation EU',      required: false },
    { excelHeader: 'Conservation MD',      modelField: 'conservation_md',      label: 'Conservation MD',      required: false },
    { excelHeader: 'Endurance',            modelField: 'endurance',            label: 'Endurance',            required: false },
    { excelHeader: 'Vitesse nage min (m/s)', modelField: 'vitesse_nage_min_ms', label: 'Vitesse min',         required: false },
    { excelHeader: 'Vitesse nage moy (m/s)', modelField: 'vitesse_nage_moy_ms', label: 'Vitesse moy',         required: false },
    { excelHeader: 'Vitesse nage max (m/s)', modelField: 'vitesse_nage_max_ms', label: 'Vitesse max',         required: false },
  ];

  createFn = (row: any) => this.nonPoissonsService.create(row);

  private searchSubject = new Subject<string>();
  private destroy$ = new Subject<void>();

  ngOnInit(): void {
    this.searchSubject.pipe(
      debounceTime(400),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    ).subscribe(() => this.appliquerFiltres());
    this.loadItems();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadItems(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.nonPoissonsService.getAll().subscribe({
      next: (response) => {
        this.allItems = [...response];
        this.appliquerFiltres();
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Erreur lors du chargement des non-poissons.';
        this.isLoading = false;
      },
    });
  }

  appliquerFiltres(): void {
    let resultats = [...this.allItems];

    if (this.searchTerm.trim()) {
      const terme = this.searchTerm.toLowerCase().trim();
      resultats = resultats.filter(p =>
        p.nom_commun?.toLowerCase().includes(terme) ||
        p.genre?.toLowerCase().includes(terme) ||
        p.espece?.toLowerCase().includes(terme) ||
        p.famille?.toLowerCase().includes(terme) ||
        p.groupe?.toLowerCase().includes(terme)
      );
    }

    if (this.selectedGroupe) {
      resultats = resultats.filter(p => p.groupe === this.selectedGroupe);
    }

    if (this.selectedGuildeEco) {
      resultats = resultats.filter(p => p.guilde_ecologique === this.selectedGuildeEco);
    }

    if (this.selectedRepartition) {
      resultats = resultats.filter(p => p.repartition_colonne_eau === this.selectedRepartition);
    }

    this.itemsFiltres = [...resultats];
    this.totalCount = this.itemsFiltres.length;
    this.currentPage = 1;
    this.cdr.detectChanges();
  }

  get itemsPage(): NonPoisson[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.itemsFiltres.slice(start, start + this.pageSize);
  }

  get totalPages(): number {
    return Math.ceil(this.totalCount / this.pageSize);
  }

  get pages(): number[] {
    const total = this.totalPages;
    if (total <= 5) return Array.from({ length: total }, (_, i) => i + 1);
    if (this.currentPage <= 3) return [1, 2, 3, 4, 5];
    if (this.currentPage >= total - 2) return [total-4, total-3, total-2, total-1, total];
    return [this.currentPage-2, this.currentPage-1, this.currentPage, this.currentPage+1, this.currentPage+2];
  }

  get startItem(): number {
    return this.totalCount === 0 ? 0 : (this.currentPage - 1) * this.pageSize + 1;
  }

  get endItem(): number {
    return Math.min(this.currentPage * this.pageSize, this.totalCount);
  }

  goToPage(page: number): void {
    if (page < 1 || page > this.totalPages) return;
    this.currentPage = page;
    this.cdr.detectChanges();
  }

  onSearchChange(): void { this.searchSubject.next(this.searchTerm); }
  onFilterChange(): void { this.appliquerFiltres(); }

  onDelete(item: NonPoisson): void { this.itemToDelete = item; }

  onConfirmDelete(): void {
    if (!this.itemToDelete) return;
    this.nonPoissonsService.delete(this.itemToDelete.id_non_poisson!).subscribe({
      next: () => { this.itemToDelete = null; this.loadItems(); },
      error: (err) => console.error(err),
    });
  }

  onCancelDelete(): void { this.itemToDelete = null; }
  onExportCsv(): void { this.nonPoissonsService.exportExcel(this.itemsFiltres); }
  onDownloadTemplate(): void { this.nonPoissonsService.downloadTemplate(); }
  onOpenImport(): void { this.showImportModal.set(true); }
  onCloseImport(): void { this.showImportModal.set(false); }
  onImportDone(): void { this.showImportModal.set(false); this.loadItems(); }

  getBadgeClass(groupe: string): string {
    return this.badgeColors[groupe] || 'badge-default';
  }
}