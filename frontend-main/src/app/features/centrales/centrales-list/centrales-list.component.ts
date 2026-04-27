import { Component, OnInit, OnDestroy, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Subject, debounceTime, distinctUntilChanged, takeUntil } from 'rxjs';
import { CentralesService } from '../../../core/services/centrales.service';
import { ImportService } from '../../../core/services/import.service';
import { ToastService } from '../../../core/services/toast.service';
import { Centrale } from '../../../models/centrale.model';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent, BreadcrumbItem } from '../../../shared/components/header/header.component';
import {
  MILIEU_TYPE_OPTIONS,
  TYPE_CIRCUIT_OPTIONS,
  CANAL_AMENEE_OPTIONS,
  MILIEU_BADGE_COLORS,
} from '../../../core/constants/centrale.constants';
import { PAGE_SIZE_DEFAULT } from '../../../core/constants/app.constants';
import { ImportModalComponent, ColumnMapping } from '../../../shared/components/import-modal/import-modal.component';
import { ConfirmDeleteModalComponent } from '../../../shared/components/confirm-delete-modal/confirm-delete-modal.component';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-centrales-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    FormsModule,
    SidebarComponent,
    HeaderComponent,
    ImportModalComponent,
    ConfirmDeleteModalComponent
  ],
  templateUrl: './centrales-list.component.html',
  styleUrl: './centrales-list.component.scss',
})
export class CentralesListComponent implements OnInit, OnDestroy {

  router = inject(Router);
  authService = inject(AuthService);
  private centralesService = inject(CentralesService);
  private importService = inject(ImportService);
  private toastService = inject(ToastService);

  centraleColumnMappings: ColumnMapping[] = [
    { excelHeader: 'Site',                          modelField: 'site_name',                    label: 'Site',                        required: true  },
    { excelHeader: 'Code',                          modelField: 'code_nom',                     label: 'Code',                        required: true  },
    { excelHeader: 'Milieu',                        modelField: 'milieu_type',                  label: 'Milieu',                      required: false },
    { excelHeader: 'Source froide',                 modelField: 'source_froide',                label: 'Source froide',               required: false },
    { excelHeader: 'Nb réacteurs',                  modelField: 'nbre_reacteurs',               label: 'Nb réacteurs',                required: false },
    { excelHeader: 'Puissance (MW)',                modelField: 'puissance_reacteurs_mwe',      label: 'Puissance (MW)',              required: false },
    { excelHeader: 'Débit aspiré par tranche (m3/s)', modelField: 'debit_aspire_par_tranche_m3s', label: 'Débit aspiré/tranche',      required: false },
    { excelHeader: 'Débit total aspiré (m3/s)',     modelField: 'debit_total_aspire_m3s',       label: 'Débit total aspiré',          required: false },
    { excelHeader: 'Disponibilité tranches',        modelField: 'taux_disponibilite_moyen_tranches', label: 'Disponibilité tranches', required: false },
    { excelHeader: 'Type circuit',                  modelField: 'type_circuit',                 label: 'Type circuit',                required: false },
    { excelHeader: 'Type filtration',               modelField: 'type_filtration',              label: 'Type filtration',             required: false },
    { excelHeader: 'Dimension filtre (h/l/m)',      modelField: 'dimension_filtre_h_l_m',       label: 'Dimension filtre',            required: false },
    { excelHeader: 'Maillage (mm)',                 modelField: 'maillage_mm',                  label: 'Maillage (mm)',               required: false },
    { excelHeader: 'Pression nettoyage',            modelField: 'pression_nettoyage',           label: 'Pression nettoyage',          required: false },
    { excelHeader: 'Traitement chimique',           modelField: 'traitement_chimique',          label: 'Traitement chimique',         required: false },
    { excelHeader: 'Type traitement chimique',      modelField: 'type_traitement_chimique',     label: 'Type traitement chimique',    required: false },
    { excelHeader: 'Circuits CRF/SEC séparés',      modelField: 'circuits_crf_sec_separes',     label: 'Circuits CRF/SEC séparés',    required: false },
    { excelHeader: 'Pompes séparées',               modelField: 'pompes_separees',              label: 'Pompes séparées',             required: false },
    { excelHeader: 'Fonctionnement filtre',         modelField: 'fonctionnement_filtre',        label: 'Fonctionnement filtre',       required: false },
    { excelHeader: 'Temps moyen émersion (min)',    modelField: 'temps_moyen_emersion_min',     label: 'Temps moyen émersion',        required: false },
    { excelHeader: 'Système récupération',          modelField: 'systeme_recuperation',         label: 'Système récupération',        required: false },
    { excelHeader: 'Présence goulotte',             modelField: 'presence_goulotte',            label: 'Présence goulotte',           required: false },
    { excelHeader: 'Goulotte hauteur eau (m)',      modelField: 'goulotte_hauteur_eau',         label: 'Goulotte hauteur eau',        required: false },
    { excelHeader: 'Présence pré-grille',           modelField: 'presence_pre_grille',          label: 'Présence pré-grille',         required: false },
    { excelHeader: 'Espacement pré-grille (mm)',    modelField: 'espacement_pre_grille_mm',     label: 'Espacement pré-grille',       required: false },
    { excelHeader: 'Canal amenée',                  modelField: 'presence_canal_amenee',        label: 'Canal amenée',                required: false },
    { excelHeader: 'Localisation prise eau',        modelField: 'localisation_prise_eau',       label: 'Localisation prise eau',      required: false },
    { excelHeader: 'Localisation rejet eau',        modelField: 'localisation_rejet_eau',       label: 'Localisation rejet eau',      required: false },
    { excelHeader: 'Profondeur rejet eau (m)',      modelField: 'profondeur_rejet_eau_m',       label: 'Profondeur rejet eau',        required: false },
    { excelHeader: 'Distance côte rejet eau (m)',   modelField: 'distance_cote_rejet_eau_m',    label: 'Distance côte rejet eau',     required: false },
    { excelHeader: 'Volume eau rejetée (m3/s)',     modelField: 'volume_eau_rejetee_m3s',       label: 'Volume eau rejetée',          required: false },
    { excelHeader: 'Température rejet (°C)',        modelField: 'temperature_rejet_c',          label: 'Température rejet',           required: false },
    { excelHeader: 'Température milieu (°C)',       modelField: 'temperature_milieu_c',         label: 'Température milieu',          required: false },
    { excelHeader: 'Delta T (°C)',                  modelField: 'delta_t_c',                    label: 'Delta T',                     required: false },
  ];

  showImportModal = signal(false);

  createCentraleFn = (row: any) => this.centralesService.create(row);

  onImportDone(result: any): void {
    this.showImportModal.set(false);
    this.loadCentrales();
  }

  onOpenImport(): void {
    this.showImportModal.set(true);
  }

  onCloseImport(): void {
    this.showImportModal.set(false);
  }

  // ─── Breadcrumb ───
  breadcrumbs: BreadcrumbItem[] = [
    { label: 'Accueil', route: '/' },
    { label: 'Centrales' },
  ];

  // ─── Données ───
  allCentrales: Centrale[] = [];
  centralesFiltrees: Centrale[] = [];
  totalCount = 0;
  isLoading = false;
  errorMessage = '';

  // ─── Filtres ───
  searchTerm = '';
  selectedMilieu = '';
  selectedTypeCircuit = '';
  selectedCanal = 'tous';

  // ─── Pagination ───
  currentPage = 1;
  pageSize = PAGE_SIZE_DEFAULT;

  // ─── Options ───
  milieuOptions = MILIEU_TYPE_OPTIONS;
  typeCircuitOptions = TYPE_CIRCUIT_OPTIONS;
  canalOptions = CANAL_AMENEE_OPTIONS;
  milieuBadgeColors = MILIEU_BADGE_COLORS;

  // ─── Search debounce ───
  private searchSubject = new Subject<string>();
  private destroy$ = new Subject<void>();

  ngOnInit(): void {
    this.searchSubject.pipe(
      debounceTime(400),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      this.appliquerFiltres();
    });
    this.loadCentrales();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadCentrales(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.centralesService.getAll().subscribe({
      next: (response) => {
        this.allCentrales = response;
        this.isLoading = false;
        this.appliquerFiltres();
      },
      error: (err) => {
        this.errorMessage = 'Erreur lors du chargement des centrales.';
        this.isLoading = false;
        console.error(err);
      },
    });
  }

  appliquerFiltres(): void {
    let resultats = [...this.allCentrales];

    if (this.searchTerm.trim()) {
      const terme = this.searchTerm.toLowerCase().trim();
      resultats = resultats.filter(c =>
        c.site_name?.toLowerCase().includes(terme) ||
        c.code_nom?.toLowerCase().includes(terme) ||
        c.milieu_type?.toLowerCase().includes(terme) ||
        c.source_froide?.toLowerCase().includes(terme) ||
        c.type_circuit?.toLowerCase().includes(terme) ||
        c.nbre_reacteurs?.toString().includes(terme) ||
        c.puissance_reacteurs_mwe?.toString().includes(terme)
      );
    }

    if (this.selectedMilieu) {
      resultats = resultats.filter(c => c.milieu_type === this.selectedMilieu);
    }

    if (this.selectedTypeCircuit) {
      resultats = resultats.filter(c => c.type_circuit === this.selectedTypeCircuit);
    }

    if (this.selectedCanal === 'oui') {
      resultats = resultats.filter(c => c.presence_canal_amenee === true);
    } else if (this.selectedCanal === 'non') {
      resultats = resultats.filter(c => c.presence_canal_amenee === false);
    }

    this.centralesFiltrees = [...resultats];
    this.totalCount = this.centralesFiltrees.length;
    this.currentPage = 1;
  }

  get centralesPage(): Centrale[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.centralesFiltrees.slice(start, start + this.pageSize);
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

  onCanalChange(value: string): void {
    this.selectedCanal = value;
    this.appliquerFiltres();
  }

  onExportCsv(): void {
    this.centralesService.exportExcel(this.centralesFiltrees);
  }

  onDownloadTemplate(): void {
    this.centralesService.downloadTemplate();
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
    const import$ = await this.centralesService.importFile(file);
    import$.subscribe({
      next: (result) => {
        this.isLoading = false;
        if (result.errors.length > 0) {
          this.errorMessage = `${result.success}/${result.total} lignes importées. ${result.errors.length} erreurs.`;
        }
        this.loadCentrales();
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = 'Erreur lors de l\'import';
        console.error(err);
      },
    });
  }

  getBadgeClass(milieu: string): string {
    return this.milieuBadgeColors[milieu] || 'badge-default';
  }

  get startItem(): number {
    return this.totalCount === 0 ? 0 : (this.currentPage - 1) * this.pageSize + 1;
  }

  get endItem(): number {
    return Math.min(this.currentPage * this.pageSize, this.totalCount);
  }

  centraleToDelete: Centrale | null = null;

  onDelete(centrale: Centrale): void {
    this.centraleToDelete = centrale;
  }

  onConfirmDelete(): void {
    if (!this.centraleToDelete) return;
    const id = this.centraleToDelete.id!;
    this.centralesService.delete(id).subscribe({
      next: () => {
        this.allCentrales = this.allCentrales.filter(c => c.id !== id);
        this.centraleToDelete = null;
        this.appliquerFiltres();
        this.toastService.success('Centrale supprimée avec succès');
      },
      error: (err) => {
        console.error(err);
        this.toastService.error('Erreur lors de la suppression de la centrale');
      },
    });
  }

  onCancelDelete(): void {
    this.centraleToDelete = null;
  }
}
