import { Component, OnInit, OnDestroy, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Subject, debounceTime, distinctUntilChanged, takeUntil } from 'rxjs';

import { PoissonsService } from '../../../core/services/poissons.service';
import { Poisson } from '../../../models/poisson.model';
import { AuthService } from '../../../core/services/auth.service';
import { ImportService } from '../../../core/services/import.service';
import { ToastService } from '../../../core/services/toast.service';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent, BreadcrumbItem } from '../../../shared/components/header/header.component';
import { ImportModalComponent, ColumnMapping } from '../../../shared/components/import-modal/import-modal.component';
import { ConfirmDeleteModalComponent } from '../../../shared/components/confirm-delete-modal/confirm-delete-modal.component';
import {
  GUILDE_ECOLOGIQUE_OPTIONS,
  REPARTITION_COLONNE_EAU_OPTIONS,
  GUILDE_TROPHIQUE_OPTIONS,
  POISSON_BADGE_COLORS,
} from '../../../core/constants/poisson.constants';
import { PAGE_SIZE_DEFAULT } from '../../../core/constants/app.constants';

@Component({
  selector: 'app-poissons-list',
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
  templateUrl: './poissons-list.component.html',
  styleUrl: './poissons-list.component.scss',
})
export class PoissonsListComponent implements OnInit, OnDestroy {

  private poissonsService = inject(PoissonsService);
  private importService = inject(ImportService);
  private toastService = inject(ToastService);
  router = inject(Router);
  authService = inject(AuthService);

  breadcrumbs: BreadcrumbItem[] = [
    { label: 'Accueil', route: '/accueil' },
    { label: 'Poissons' },
  ];

  // ─── Données ───
  allPoissons: Poisson[] = [];
  poissonsFiltres: Poisson[] = [];
  totalCount = 0;
  isLoading = false;
  errorMessage = '';

  // ─── Filtres ───
  searchTerm = '';
  selectedGuildeEco = '';
  selectedRepartition = '';
  selectedGuilde = '';

  // ─── Pagination ───
  currentPage = 1;
  pageSize = PAGE_SIZE_DEFAULT;

  // ─── Options ───
  guildeEcoOptions = GUILDE_ECOLOGIQUE_OPTIONS;
  repartitionOptions = REPARTITION_COLONNE_EAU_OPTIONS;
  guildeTrophiqueOptions = GUILDE_TROPHIQUE_OPTIONS;
  badgeColors = POISSON_BADGE_COLORS;

  // ─── Modals ───
  showImportModal = signal(false);
  poissonToDelete: Poisson | null = null;

  // ─── Search debounce ───
  private searchSubject = new Subject<string>();
  private destroy$ = new Subject<void>();

  // ─── Import mappings ───
  poissonColumnMappings: ColumnMapping[] = [
    { excelHeader: 'Famille',             modelField: 'famille',              label: 'Famille',             required: true  },
    { excelHeader: 'Genre',               modelField: 'genre',                label: 'Genre',               required: true  },
    { excelHeader: 'Espèce',              modelField: 'espece',               label: 'Espèce',              required: true  },
    { excelHeader: 'Nom commun',          modelField: 'nom_commun',           label: 'Nom commun',          required: true  },
    { excelHeader: 'Guilde écologique',   modelField: 'guilde_ecologique',    label: 'Guilde écologique',   required: false },
    { excelHeader: 'Répartition colonne eau', modelField: 'repartition_colonne_eau', label: 'Répartition colonne eau', required: false },
    { excelHeader: 'Guilde trophique',    modelField: 'guilde_trophique',     label: 'Guilde trophique',    required: false },
    { excelHeader: 'Intérêt halieutique', modelField: 'interet_halieutique',  label: 'Intérêt halieutique', required: false },
    { excelHeader: 'État stock',          modelField: 'etat_stock',           label: 'État stock',          required: false },
    { excelHeader: 'Statut protection',   modelField: 'statut_protection',    label: 'Statut protection',   required: false },
    { excelHeader: 'Conservation FR',     modelField: 'conservation_fr',      label: 'Conservation FR',     required: false },
    { excelHeader: 'Conservation EU',     modelField: 'conservation_eu',      label: 'Conservation EU',     required: false },
    { excelHeader: 'Conservation MD',     modelField: 'conservation_md',      label: 'Conservation MD',     required: false },
    { excelHeader: 'Comportement',        modelField: 'comportement',         label: 'Comportement',        required: false },
    { excelHeader: 'Forme corps',         modelField: 'forme_corps',          label: 'Forme corps',         required: false },
    { excelHeader: 'Locomotion',          modelField: 'locomotion',           label: 'Locomotion',          required: false },
  ];

  createPoissonFn = (row: any) => this.poissonsService.create(row);

  ngOnInit(): void {
    this.searchSubject.pipe(
      debounceTime(400),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      this.appliquerFiltres();
    });
    this.loadPoissons();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadPoissons(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.poissonsService.getAll().subscribe({
      next: (response) => {
        this.allPoissons = [...response];
        this.isLoading = false;
        this.appliquerFiltres();
      },
      error: (err) => {
        this.errorMessage = 'Erreur lors du chargement des poissons.';
        this.isLoading = false;
        console.error(err);
      },
    });
  }

  appliquerFiltres(): void {
    let resultats = [...this.allPoissons];

    if (this.searchTerm.trim()) {
      const terme = this.searchTerm.toLowerCase().trim();
      resultats = resultats.filter(p =>
        p.famille?.toLowerCase().includes(terme) ||
        p.genre?.toLowerCase().includes(terme) ||
        p.espece?.toLowerCase().includes(terme) ||
        p.nom_commun?.toLowerCase().includes(terme) ||
        p.guilde_ecologique?.toLowerCase().includes(terme)
      );
    }

    if (this.selectedGuildeEco) {
      resultats = resultats.filter(p => p.guilde_ecologique === this.selectedGuildeEco);
    }

    if (this.selectedRepartition) {
      resultats = resultats.filter(p => p.repartition_colonne_eau === this.selectedRepartition);
    }

    if (this.selectedGuilde) {
      resultats = resultats.filter(p => p.guilde_trophique === this.selectedGuilde);
    }

    this.poissonsFiltres = [...resultats];
    this.totalCount = this.poissonsFiltres.length;
    this.currentPage = 1;
  }

  get poissonsPage(): Poisson[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.poissonsFiltres.slice(start, start + this.pageSize);
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
  }

  onSearchChange(): void {
    this.searchSubject.next(this.searchTerm);
  }

  onFilterChange(): void {
    this.appliquerFiltres();
  }

  onDelete(poisson: Poisson): void {
    this.poissonToDelete = poisson;
  }

  onConfirmDelete(): void {
    if (!this.poissonToDelete) return;
    const id = this.poissonToDelete.id_poisson!;
    this.poissonsService.delete(id).subscribe({
      next: () => {
        this.allPoissons = this.allPoissons.filter(p => p.id_poisson !== id);
        this.poissonToDelete = null;
        this.appliquerFiltres();
        this.toastService.success('Poisson supprimé avec succès');
      },
      error: (err) => {
        console.error(err);
        this.toastService.error('Erreur lors de la suppression du poisson');
      },
    });
  }

  onCancelDelete(): void {
    this.poissonToDelete = null;
  }

  onExportCsv(): void {
    this.poissonsService.exportExcel(this.poissonsFiltres);
  }

  onDownloadTemplate(): void {
    this.poissonsService.downloadTemplate();
  }

  async onImport(event: Event): Promise<void> {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;
    const file = input.files[0];
    const validation = this.importService.validateFile(file);
    if (!validation.valid) {
      this.errorMessage = validation.error || 'Fichier invalide';
      return;
    }
    this.isLoading = true;
    const import$ = await this.poissonsService.importFile(file);
    import$.subscribe({
      next: (result) => {
        this.isLoading = false;
        if (result.errors.length > 0) {
          this.errorMessage = `${result.success}/${result.total} lignes importées. ${result.errors.length} erreurs.`;
        }
        this.loadPoissons();
      },
      error: () => {
        this.isLoading = false;
        this.errorMessage = 'Erreur lors de l\'import';
      },
    });
  }

  onOpenImport(): void { this.showImportModal.set(true); }
  onCloseImport(): void { this.showImportModal.set(false); }
  onImportDone(): void { this.showImportModal.set(false); this.loadPoissons(); }

  getBadgeClass(guilde: string): string {
    return this.badgeColors[guilde] || 'badge-default';
  }
}
