import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AbstractControl, ReactiveFormsModule, FormBuilder, FormGroup, ValidationErrors, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CentralesService } from '../../../core/services/centrales.service';
import {
  MILIEU_TYPE_OPTIONS,
  TYPE_CIRCUIT_OPTIONS,
  TYPE_FILTRATION_OPTIONS,
  PRESSION_NETTOYAGE_OPTIONS,
  TYPE_TRAITEMENT_CHIMIQUE_OPTIONS,
  FONCTIONNEMENT_FILTRE_OPTIONS,
  LOCALISATION_OPTIONS,
} from '../../../core/constants/centrale.constants';

import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent } from '../../../shared/components/header/header.component';
import { SectionHeader } from '../../../shared/components/section-header/section-header';
import { FieldInputComponent } from '../../../shared/components/field-input/field-input.component';
import { FieldSelectComponent } from '../../../shared/components/field-select/field-select.component';
import { FieldToggleComponent } from '../../../shared/components/field-toggle/field-toggle.component';

function integerValidator(control: AbstractControl): ValidationErrors | null {
  const v = control.value;
  if (v === null || v === '' || v === undefined) return null;
  return Number.isInteger(Number(v)) ? null : { integer: true };
}

@Component({
  selector: 'app-centrales-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    SidebarComponent,
    HeaderComponent,
    SectionHeader,
    FieldInputComponent,
    FieldSelectComponent,
    FieldToggleComponent,
  ],
  templateUrl: './centrales-form.component.html',
  styleUrl: './centrales-form.component.scss'
})
export class CentralesFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private centralesService = inject(CentralesService);

  breadcrumbs = [
    { label: 'Centrales', route: '/centrales' },
    { label: 'Nouvelle centrale' },
  ];

  form!: FormGroup;
  isEdit = false;
  centraleId: number | null = null;
  loading = false;
  saving = false;
  activeTab: 'site' | 'circuit' | 'prise_eau' | 'courantologie' = 'site';

  milieuOptions = MILIEU_TYPE_OPTIONS.filter(o => o.value !== '');
  circuitOptions = TYPE_CIRCUIT_OPTIONS.filter(o => o.value !== '');
  filtrationOptions = TYPE_FILTRATION_OPTIONS.filter(o => o.value !== '');
  pressionOptions = PRESSION_NETTOYAGE_OPTIONS.filter(o => o.value !== '');
  traitementOptions = TYPE_TRAITEMENT_CHIMIQUE_OPTIONS;
  fonctionnementFiltreOptions = FONCTIONNEMENT_FILTRE_OPTIONS.filter(o => o.value !== '');
  localisationOptions = LOCALISATION_OPTIONS.filter(o => o.value !== '');

  ngOnInit(): void {
    this.buildForm();
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEdit = true;
      this.centraleId = Number(id);
      this.loading = true;
      this.breadcrumbs[1].label = 'Modifier la centrale';
      this.centralesService.getById(this.centraleId).subscribe({
        next: (c) => { this.form.patchValue(c); this.loading = false; },
        error: () => { this.loading = false; }
      });
    }
  }

  buildForm(): void {
    this.form = this.fb.group({
      code_nom: ['', Validators.required],
      site_name: ['', Validators.required],
      milieu_type: [''],
      source_froide: [''],
      nbre_reacteurs: [null, [integerValidator]],
      puissance_reacteurs_mwe: [null],
      debit_aspire_par_tranche_m3s: [null],
      debit_total_aspire_m3s: [null],
      taux_disponibilite_moyen_tranches: [''],
      notes: [''],

      type_circuit: [''],
      type_filtration: [''],
      dimension_filtre_h_l_m: [''],
      maillage_mm: [null, [integerValidator]],
      pression_nettoyage: [''],
      traitement_chimique: [null],
      type_traitement_chimique: [''],
      circuits_crf_sec_separes: [null],
      pompes_separees: [null],
      fonctionnement_filtre: [''],
      temps_moyen_emersion_min: [null, [integerValidator]],
      systeme_recuperation: [null],
      presence_goulotte: [null],
      goulotte_hauteur_eau: [null, [integerValidator]],
      presence_pre_grille: [null],
      espacement_pre_grille_mm: [null, [integerValidator]],

      presence_canal_amenee: [null],
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

  setTab(tab: typeof this.activeTab): void {
    this.activeTab = tab;
  }

  onSubmit(): void {
    this.form.markAllAsTouched();
    if (this.form.invalid) return;
    this.saving = true;
    const data = this.form.getRawValue();

    const obs = this.isEdit && this.centraleId
      ? this.centralesService.update(this.centraleId, data)
      : this.centralesService.create(data);

    obs.subscribe({
      next: (c) => {
        this.saving = false;
        this.router.navigate(['/centrales', c.id]);
      },
      error: () => { this.saving = false; }
    });
  }

  onCancel(): void {
    if (this.isEdit && this.centraleId) {
      this.router.navigate(['/centrales', this.centraleId]);
    } else {
      this.router.navigate(['/centrales']);
    }
  }
}
