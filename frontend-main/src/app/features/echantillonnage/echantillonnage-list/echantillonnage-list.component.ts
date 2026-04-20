import { Component, OnInit, OnDestroy, inject, signal, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Subject, debounceTime, distinctUntilChanged, takeUntil } from 'rxjs';

import { EchantillonnageService } from '../../../core/services/echantillonnage.service';
import { Echantillonnage } from '../../../models/echantillonnage.model';
import { AuthService } from '../../../core/services/auth.service';
import { ImportService } from '../../../core/services/import.service';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent, BreadcrumbItem } from '../../../shared/components/header/header.component';
import { ImportModalComponent, ColumnMapping } from '../../../shared/components/import-modal/import-modal.component';
import { ConfirmDeleteModalComponent } from '../../../shared/components/confirm-delete-modal/confirm-delete-modal.component';
import {
  GROUPE_OPTIONS,
  FREQUENCE_OCCURRENCE_OPTIONS,
  ECHANTILLONNAGE_BADGE_COLORS,
} from '../../../core/constants/echantillonnage.constants';
import { PAGE_SIZE_DEFAULT } from '../../../core/constants/app.constants';

@Component({
  selector: 'app-echantillonnage-list',
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
  templateUrl: './echantillonnage-list.component.html',
  styleUrl: './echantillonnage-list.component.scss',
})
export class EchantillonnageListComponent implements OnInit, OnDestroy {

  private echantillonnageService = inject(EchantillonnageService);
  private importService = inject(ImportService);
  private cdr = inject(ChangeDetectorRef);
  router = inject(Router);
  authService = inject(AuthService);

  breadcrumbs: BreadcrumbItem[] = [
    { label: 'Accueil', route: '/accueil' },
    { label: 'Échantillonnage' },
  ];

  allItems: Echantillonnage[] = [];
  itemsFiltres: Echantillonnage[] = [];
  totalCount = 0;
  isLoading = false;
  errorMessage = '';

  searchTerm = '';
  selectedGroupe = '';
  selectedFrequence = '';

  currentPage = 1;
  pageSize = PAGE_SIZE_DEFAULT;

  groupeOptions = GROUPE_OPTIONS;
  frequenceOptions = FREQUENCE_OCCURRENCE_OPTIONS;
  badgeColors = ECHANTILLONNAGE_BADGE_COLORS;

  showImportModal = signal(false);
  itemToDelete: Echantillonnage | null = null;

  columnMappings: ColumnMapping[] = [
    { excelHeader: 'Centrale',            modelField: 'centrale',                 label: 'Centrale',            required: true  },
    { excelHeader: 'Date',                modelField: 'date_echantillonnage',      label: 'Date',                required: true  },
    { excelHeader: 'Nb échantillonnage',  modelField: 'nombre_echantillonnage',    label: 'Nb échantillonnage',  required: false },
    { excelHeader: 'Durée (min)',         modelField: 'duree_echantillonnage_min', label: 'Durée (min)',         required: false },
    { excelHeader: 'Débris végétaux',     modelField: 'debris_vegetaux',           label: 'Débris végétaux',     required: false },
    { excelHeader: 'Groupe',             modelField: 'groupe',                    label: 'Groupe',              required: false },
    { excelHeader: 'Poisson',            modelField: 'poisson',                   label: 'Poisson',             required: false },
    { excelHeader: 'Non-poisson',        modelField: 'non_poisson',               label: 'Non-poisson',         required: false },
    { excelHeader: 'Fréquence occurrence', modelField: 'frequence_occurrence',    label: 'Fréquence occurrence', required: false },
  ];

  createFn = (row: any) => this.echantillonnageService.create(row);

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
    this.echantillonnageService.getAll().subscribe({
      next: (response) => {
        this.allItems = [...response];
        this.appliquerFiltres();
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Erreur lors du chargement des échantillonnages.';
        this.isLoading = false;
      },
    });
  }

  appliquerFiltres(): void {
    let resultats = [...this.allItems];

    if (this.searchTerm.trim()) {
      const terme = this.searchTerm.toLowerCase().trim();
      resultats = resultats.filter(e =>
        e.centrale_label?.toLowerCase().includes(terme) ||
        e.date_echantillonnage?.toLowerCase().includes(terme) ||
        e.poisson_label?.toLowerCase().includes(terme) ||
        e.non_poisson_label?.toLowerCase().includes(terme) ||
        e.groupe?.toLowerCase().includes(terme)
      );
    }

    if (this.selectedGroupe) {
      resultats = resultats.filter(e => e.groupe === this.selectedGroupe);
    }

    if (this.selectedFrequence) {
      resultats = resultats.filter(e => e.frequence_occurrence === this.selectedFrequence);
    }

    this.itemsFiltres = [...resultats];
    this.totalCount = this.itemsFiltres.length;
    this.currentPage = 1;
    this.cdr.detectChanges();
  }

  get itemsPage(): Echantillonnage[] {
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

  onDelete(item: Echantillonnage): void { this.itemToDelete = item; }

  onConfirmDelete(): void {
    if (!this.itemToDelete) return;
    this.echantillonnageService.delete(this.itemToDelete.id_echantillonnage!).subscribe({
      next: () => { this.itemToDelete = null; this.loadItems(); },
      error: (err) => console.error(err),
    });
  }

  onCancelDelete(): void { this.itemToDelete = null; }
  onExportCsv(): void { this.echantillonnageService.exportExcel(this.itemsFiltres); }
  onDownloadTemplate(): void { this.echantillonnageService.downloadTemplate(); }
  onOpenImport(): void { this.showImportModal.set(true); }
  onCloseImport(): void { this.showImportModal.set(false); }
  onImportDone(): void { this.showImportModal.set(false); this.loadItems(); }

  getBadgeClass(groupe: string): string {
    return this.badgeColors[groupe] || 'badge-default';
  }

  getItemLabel(item: Echantillonnage): string {
    return `#${item.id_echantillonnage} — ${item.centrale_label || 'Site ?'} — ${item.date_echantillonnage || 'Date ?'}`;
  }
}