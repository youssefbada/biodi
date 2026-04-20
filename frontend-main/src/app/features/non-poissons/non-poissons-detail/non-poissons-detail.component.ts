import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { NonPoissonsService } from '../../../core/services/non-poissons.service';
import { NonPoisson } from '../../../models/non-poisson.model';
import { AuthService } from '../../../core/services/auth.service';
import { ConfirmLeaveService } from '../../../core/services/confirm-leave.service';
import { CanComponentDeactivate } from '../../../core/guards/confirm-leave.guard';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent } from '../../../shared/components/header/header.component';
import { SectionHeader } from '../../../shared/components/section-header/section-header';
import { FieldInputComponent } from '../../../shared/components/field-input/field-input.component';
import { FieldSelectComponent } from '../../../shared/components/field-select/field-select.component';
import { FieldToggleComponent } from '../../../shared/components/field-toggle/field-toggle.component';
import { ConfirmLeaveModalComponent } from '../../../shared/components/confirm-leave-modal/confirm-leave-modal.component';
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
  selector: 'app-non-poissons-detail',
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
    ConfirmLeaveModalComponent,
  ],
  templateUrl: './non-poissons-detail.component.html',
  styleUrl: './non-poissons-detail.component.scss',
})
export class NonPoissonsDetailComponent implements OnInit, CanComponentDeactivate {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private fb = inject(FormBuilder);
  private nonPoissonsService = inject(NonPoissonsService);
  authService = inject(AuthService);
  confirmLeaveService = inject(ConfirmLeaveService);

  item: NonPoisson | null = null;
  loading = true;
  error = false;
  editing = false;
  saving = false;
  saved = false;
  activeTab: 'identite' | 'ecologie' | 'nage' = 'identite';

  form!: FormGroup;

  breadcrumbs = [
    { label: 'Non-poissons', route: '/non-poissons' },
    { label: 'Fiche détail' },
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

  isEditing(): boolean { return this.editing; }

  ngOnInit(): void {
    this.buildForm();
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.nonPoissonsService.getById(id).subscribe({
      next: (p) => {
        this.item = p;
        this.form.patchValue(p);
        this.breadcrumbs[1].label = `Fiche – ${p.nom_commun || p.genre + ' ' + p.espece}`;
        this.loading = false;
      },
      error: () => { this.error = true; this.loading = false; }
    });
  }

  buildForm(): void {
    this.form = this.fb.group({
      groupe: [''],
      famille: [''],
      genre: [''],
      espece: [''],
      nom_commun: [''],
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

  startEdit(): void {
    if (!this.item) return;
    this.form.patchValue(this.item);
    this.editing = true;
    this.saved = false;
  }

  cancelEdit(): void {
    this.editing = false;
    if (this.item) this.form.patchValue(this.item);
  }

  saveEdit(): void {
    if (!this.item || this.form.invalid) return;
    this.saving = true;
    const id = this.item.id_non_poisson;
    if (id === undefined) return;
    this.nonPoissonsService.update(id, this.form.getRawValue()).subscribe({
      next: (updated) => {
        this.item = updated;
        this.form.patchValue(updated);
        this.editing = false;
        this.saving = false;
        this.saved = true;
        setTimeout(() => (this.saved = false), 3000);
      },
      error: () => { this.saving = false; }
    });
  }

  get hasChanges(): boolean {
    if (!this.item) return false;
    const current = this.form.getRawValue();
    for (const key of Object.keys(current)) {
      const a = current[key] === '' || current[key] === undefined ? null : current[key];
      const b = (this.item as any)[key] === '' || (this.item as any)[key] === undefined ? null : (this.item as any)[key];
      // eslint-disable-next-line eqeqeq
      if (a != b) return true;
    }
    return false;
  }

  goBack(): void { this.router.navigate(['/non-poissons']); }
}