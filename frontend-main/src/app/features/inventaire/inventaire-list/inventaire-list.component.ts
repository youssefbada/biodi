import { Component, OnInit, OnDestroy, inject, signal, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Subject, debounceTime, distinctUntilChanged, takeUntil } from 'rxjs';

import { InventaireService } from '../../../core/services/inventaire.service';
import { Inventaire } from '../../../models/inventaire.model';
import { AuthService } from '../../../core/services/auth.service';
import { ImportService } from '../../../core/services/import.service';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent, BreadcrumbItem } from '../../../shared/components/header/header.component';
import { ImportModalComponent, ColumnMapping } from '../../../shared/components/import-modal/import-modal.component';
import { ConfirmDeleteModalComponent } from '../../../shared/components/confirm-delete-modal/confirm-delete-modal.component';
import { GROUPE_OPTIONS } from '../../../core/constants/non-poisson.constants';
import { PAGE_SIZE_DEFAULT } from '../../../core/constants/app.constants';

@Component({
  selector: 'app-inventaire-list',
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
  templateUrl: './inventaire-list.component.html',
  styleUrl: './inventaire-list.component.scss',
})
export class InventaireListComponent implements OnInit, OnDestroy {

  private inventaireService = inject(InventaireService);
  private importService = inject(ImportService);
  private cdr = inject(ChangeDetectorRef);
  router = inject(Router);
  authService = inject(AuthService);

  breadcrumbs: BreadcrumbItem[] = [
    { label: 'Accueil', route: '/accueil' },
    { label: 'Inventaire' },
  ];

  allItems: Inventaire[] = [];
  itemsFiltres: Inventaire[] = [];
  totalCount = 0;
  isLoading = false;
  errorMessage = '';

  searchTerm = '';
  selectedGroupe = '';

  currentPage = 1;
  pageSize = PAGE_SIZE_DEFAULT;

  groupeOptions = GROUPE_OPTIONS;

  showImportModal = signal(false);
  itemToDelete: Inventaire | null = null;

  columnMappings: ColumnMapping[] = [
    { excelHeader: 'Centrale',           modelField: 'centrale_id',              label: 'Centrale',           required: true  },
    { excelHeader: 'Nom commun',         modelField: 'nom_commun',               label: 'Nom commun',         required: false },
    { excelHeader: 'Groupe poisson',     modelField: 'groupe_poisson',           label: 'Groupe poisson',     required: false },
    { excelHeader: 'Espèce poisson',     modelField: 'espece_poisson_id',        label: 'Espèce poisson',     required: false },
    { excelHeader: 'Groupe non-poisson', modelField: 'groupe_non_poisson',       label: 'Groupe non-poisson', required: false },
    { excelHeader: 'Espèce non-poisson', modelField: 'espece_non_poisson_id',    label: 'Espèce non-poisson', required: false },
  ];

  createFn = (row: any) => this.inventaireService.create(row);

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
    this.inventaireService.getAll().subscribe({
      next: (response) => {
        this.allItems = [...response];
        this.appliquerFiltres();
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Erreur lors du chargement des inventaires.';
        this.isLoading = false;
      },
    });
  }

  appliquerFiltres(): void {
    let resultats = [...this.allItems];

    if (this.searchTerm.trim()) {
      const terme = this.searchTerm.toLowerCase().trim();
      resultats = resultats.filter(i =>
        i.nom_commun?.toLowerCase().includes(terme) ||
        i.centrale_label?.toLowerCase().includes(terme) ||
        i.espece_poisson_label?.toLowerCase().includes(terme) ||
        i.espece_non_poisson_label?.toLowerCase().includes(terme) ||
        i.groupe_poisson?.toLowerCase().includes(terme) ||
        i.groupe_non_poisson?.toLowerCase().includes(terme)
      );
    }

    if (this.selectedGroupe) {
      resultats = resultats.filter(i =>
        i.groupe_poisson === this.selectedGroupe ||
        i.groupe_non_poisson === this.selectedGroupe
      );
    }

    this.itemsFiltres = [...resultats];
    this.totalCount = this.itemsFiltres.length;
    this.currentPage = 1;
    this.cdr.detectChanges();
  }

  get itemsPage(): Inventaire[] {
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

  onDelete(item: Inventaire): void { this.itemToDelete = item; }

  onConfirmDelete(): void {
    if (!this.itemToDelete) return;
    this.inventaireService.delete(this.itemToDelete.id_inventaire!).subscribe({
      next: () => { this.itemToDelete = null; this.loadItems(); },
      error: (err) => console.error(err),
    });
  }

  onCancelDelete(): void { this.itemToDelete = null; }
  onExportCsv(): void { this.inventaireService.exportExcel(this.itemsFiltres); }
  onDownloadTemplate(): void { this.inventaireService.downloadTemplate(); }
  onOpenImport(): void { this.showImportModal.set(true); }
  onCloseImport(): void { this.showImportModal.set(false); }
  onImportDone(): void { this.showImportModal.set(false); this.loadItems(); }

  getItemLabel(item: Inventaire): string {
    return item.nom_commun || item.espece_poisson_label || item.espece_non_poisson_label || `Inventaire #${item.id_inventaire}`;
  }
}