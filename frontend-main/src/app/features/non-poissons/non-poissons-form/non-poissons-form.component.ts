import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { NonPoissonsService } from '../../../core/services/non-poissons.service';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent } from '../../../shared/components/header/header.component';
import { SectionHeader } from '../../../shared/components/section-header/section-header';
import { FieldInputComponent } from '../../../shared/components/field-input/field-input.component';
import { FieldSelectComponent } from '../../../shared/components/field-select/field-select.component';
import { FieldToggleComponent } from '../../../shared/components/field-toggle/field-toggle.component';
import {
  GROUPE_OPTIONS,
  GUILDE_ECOLOGIQUE_OPTIONS,
  REPARTITION_COLONNE_EAU_OPTIONS,
  GUILDE_TROPHIQUE_OPTIONS,
  ETAT_STOCK_OPTIONS,
  STATUT_PROTECTION_OPTIONS,
  CONSERVATION_OPTIONS,
  SENSIBILITE_LUMIERE_OPTIONS,
  SENSIBILITE_COURANT_OPTIONS,
  RESISTANCE_CHOCS_OPTIONS,
} from '../../../core/constants/non-poisson.constants';

@Component({
  selector: 'app-non-poissons-form',
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
  templateUrl: './non-poissons-form.component.html',
  styleUrl: './non-poissons-form.component.scss',
})
export class NonPoissonsFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private nonPoissonsService = inject(NonPoissonsService);

  form!: FormGroup;
  isEdit = false;
  itemId: number | null = null;
  loading = false;
  saving = false;
  activeTab: 'identite' | 'ecologie' | 'nage' = 'identite';

  breadcrumbs = [
    { label: 'Non-poissons', route: '/non-poissons' },
    { label: 'Nouveau non-poisson' },
  ];

  groupeOptions = GROUPE_OPTIONS.filter(o => o.value !== '');
  guildeEcoOptions = GUILDE_ECOLOGIQUE_OPTIONS.filter(o => o.value !== '');
  repartitionOptions = REPARTITION_COLONNE_EAU_OPTIONS.filter(o => o.value !== '');
  guildeTrophiqueOptions = GUILDE_TROPHIQUE_OPTIONS.filter(o => o.value !== '');
  etatStockOptions = ETAT_STOCK_OPTIONS.filter(o => o.value !== '');
  statutProtectionOptions = STATUT_PROTECTION_OPTIONS.filter(o => o.value !== '');
  conservationOptions = CONSERVATION_OPTIONS;
  sensibiliteLumiereOptions = SENSIBILITE_LUMIERE_OPTIONS.filter(o => o.value !== '');
  sensibiliteCourantOptions = SENSIBILITE_COURANT_OPTIONS.filter(o => o.value !== '');
  resistanceOptions = RESISTANCE_CHOCS_OPTIONS.filter(o => o.value !== '');

  ngOnInit(): void {
    this.buildForm();
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEdit = true;
      this.itemId = Number(id);
      this.loading = true;
      this.breadcrumbs[1].label = 'Modifier le non-poisson';
      this.nonPoissonsService.getById(this.itemId).subscribe({
        next: (p) => { this.form.patchValue(p); this.loading = false; },
        error: () => { this.loading = false; }
      });
    }
  }

  buildForm(): void {
    this.form = this.fb.group({
      groupe: [''],
      famille: [''],
      genre: [''],
      espece: [''],
      nom_commun: ['', Validators.required],
      guilde_ecologique: [''],
      source_guilde_ecolo: [''],
      repartition_colonne_eau: [''],
      source_repartition_col_eau: [''],
      guilde_trophique: [''],
      source_guilde_trophique: [''],
      enjeu_halieutique: [null],
      source_enjeu_halieutique: [''],
      etat_stock: [''],
      source_stock: [''],
      statut_protection: [''],
      source_protection: [''],
      conservation_fr: [''],
      conservation_eu: [''],
      conservation_md: [''],
      source_conservation: [''],
      sensibilite_lumiere: [''],
      source_sens_lumiere: [''],
      sensibilite_courants_eau: [''],
      source_sens_courant: [''],
      sensibilite_sonore: [''],
      source_sens_sonore: [''],
      resistance_chocs_mecaniques: [''],
      resistance_chocs_chimiques: [''],
      resistance_chocs_thermiques: [''],
      source_resistance_chocs: [''],
      endurance: [''],
      source_endurance: [''],
      vitesse_nage_min_ms: [null],
      vitesse_nage_moy_ms: [null],
      vitesse_nage_max_ms: [null],
      source_vitesse_nage: [''],
    });
  }

  setTab(tab: typeof this.activeTab): void { this.activeTab = tab; }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.saving = true;
    const data = this.form.getRawValue();
    const obs = this.isEdit && this.itemId
      ? this.nonPoissonsService.update(this.itemId, data)
      : this.nonPoissonsService.create(data);
    obs.subscribe({
      next: (p) => {
        this.saving = false;
        this.router.navigate(['/non-poissons', p.id_non_poisson]);
      },
      error: () => { this.saving = false; }
    });
  }

  onCancel(): void {
    if (this.isEdit && this.itemId) {
      this.router.navigate(['/non-poissons', this.itemId]);
    } else {
      this.router.navigate(['/non-poissons']);
    }
  }
}