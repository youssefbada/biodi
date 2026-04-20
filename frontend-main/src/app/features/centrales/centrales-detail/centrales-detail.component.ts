import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CentralesService } from '../../../core/services/centrales.service';
import { Centrale } from '../../../models/centrale.model';
import {
  MILIEU_TYPE_OPTIONS,
  TYPE_CIRCUIT_OPTIONS,
  TYPE_FILTRATION_OPTIONS,
  PRESSION_NETTOYAGE_OPTIONS,
} from '../../../core/constants/centrale.constants';
import { FieldInputComponent } from '../../../shared/components/field-input/field-input.component';
import { FieldSelectComponent } from '../../../shared/components/field-select/field-select.component';
import { FieldToggleComponent } from '../../../shared/components/field-toggle/field-toggle.component';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent } from '../../../shared/components/header/header.component';
import { SectionHeader } from '../../../shared/components/section-header/section-header';
import { ConfirmLeaveService } from '../../../core/services/confirm-leave.service';
import { CanComponentDeactivate } from '../../../core/guards/confirm-leave.guard';
import { ConfirmLeaveModalComponent } from '../../../shared/components/confirm-leave-modal/confirm-leave-modal.component';
import {
  MILIEU_BADGE_COLORS,
} from '../../../core/constants/centrale.constants';
@Component({
  selector: 'app-centrales-detail',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    SidebarComponent,
    HeaderComponent,
    FieldInputComponent,
    FieldSelectComponent,
    FieldToggleComponent,
    SectionHeader,
    ConfirmLeaveModalComponent,
  ],
  templateUrl: './centrales-detail.component.html',
  styleUrl: './centrales-detail.component.scss'
})
export class CentralesDetailComponent implements OnInit, CanComponentDeactivate {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private fb = inject(FormBuilder);
  private centralesService = inject(CentralesService);
  confirmLeaveService = inject(ConfirmLeaveService);

  centrale: Centrale | null = null;
  loading = true;
  error = false;
  editing = false;
  saving = false;
  saved = false;
  activeTab: 'site' | 'circuit' | 'prise_eau' | 'courantologie' = 'site';

  form!: FormGroup;

  breadcrumbs = [
    { label: 'Centrales', route: '/centrales' },
    { label: 'Fiche détail' },
  ];

  milieuOptions = MILIEU_TYPE_OPTIONS.filter(o => o.value !== '');
  circuitOptions = TYPE_CIRCUIT_OPTIONS.filter(o => o.value !== '');
  filtrationOptions = TYPE_FILTRATION_OPTIONS.filter(o => o.value !== '');
  pressionOptions = PRESSION_NETTOYAGE_OPTIONS.filter(o => o.value !== '');

  // ── CanComponentDeactivate ────────────────────────────────
  isEditing(): boolean {
    return this.editing;
  }

  ngOnInit(): void {
    this.buildForm();
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.centralesService.getById(id).subscribe({
      next: (c) => {
        this.centrale = c;
        this.form.patchValue(c);
        this.breadcrumbs[1].label = `Fiche – ${c.code_nom}`;
        this.loading = false;
      },
      error: () => {
        this.error = true;
        this.loading = false;
      }
    });
  }

  buildForm(): void {
    this.form = this.fb.group({
      code_nom: ['', Validators.required],
      site_name: ['', Validators.required],
      milieu_type: [''],
      source_froide: [''],
      nbre_reacteurs: [null],
      puissance_reacteurs_mwe: [null],
      debit_aspire_par_tranche_m3s: [null],
      debit_total_aspire_m3s: [null],
      taux_disponibilite_moyen_tranches: [''],
      notes: [''],
      type_circuit: [''],
      type_filtration: [''],
      dimension_filtre_h_l_m: [''],
      maillage_mm: [null],
      pression_nettoyage: [''],
      traitement_chimique: [false],
      type_traitement_chimique: [''],
      circuits_crf_sec_separes: [false],
      pompes_separees: [false],
      fonctionnement_filtre: [''],
      temps_moyen_emersion_min: [null],
      systeme_recuperation: [false],
      presence_goulotte: [false],
      goulotte_hauteur_eau: [null],
      presence_pre_grille: [false],
      espacement_pre_grille_mm: [null],
      presence_canal_amenee: [false],
      localisation_prise_eau: [''],
      localisation_rejet_eau: [''],
      profondeur_rejet_eau_m: [null],
      distance_cote_rejet_eau_m: [null],
      volume_eau_rejetee_m3s: [null],
      temperature_rejet_c: [null],
      temperature_milieu_c: [null],
      delta_t_c: [null],
    });
  }
  milieuBadgeColors = MILIEU_BADGE_COLORS;


  getBadgeClass(milieu: string): string {
    return this.milieuBadgeColors[milieu] || 'badge-default';
  }
  setTab(tab: typeof this.activeTab): void {
    this.activeTab = tab;
  }

  startEdit(): void {
    if (!this.centrale) return;
    this.form.patchValue(this.centrale);
    this.editing = true;
    this.saved = false;
  }

  cancelEdit(): void {
    this.editing = false;
    if (this.centrale) {
      this.form.patchValue(this.centrale);
    }
  }

  saveEdit(): void {
    if (!this.centrale || this.form.invalid) return;
    this.saving = true;
    const data = this.form.getRawValue();
    const id = this.centrale?.id;
    if (id === undefined) return;
    this.centralesService.update(id, data).subscribe({
      next: (updated) => {
        this.centrale = updated;
        this.form.patchValue(updated);
        this.editing = false;
        this.saving = false;
        this.saved = true;
        setTimeout(() => (this.saved = false), 3000);
      },
      error: () => {
        this.saving = false;
      }
    });
  }

  get hasChanges(): boolean {
    if (!this.centrale) return false;
    const current = this.form.getRawValue();
    for (const key of Object.keys(current)) {
      const formVal = current[key];
      const origVal = (this.centrale as any)[key];
      const a = formVal === '' || formVal === undefined ? null : formVal;
      const b = origVal === '' || origVal === undefined ? null : origVal;
      // eslint-disable-next-line eqeqeq
      if (a != b) return true;
    }
    return false;
  }

  goBack(): void {
    this.router.navigate(['/centrales']);
  }
}