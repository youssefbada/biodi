import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { PoissonsService } from '../../../core/services/poissons.service';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent } from '../../../shared/components/header/header.component';
import { SectionHeader } from '../../../shared/components/section-header/section-header';
import { FieldInputComponent } from '../../../shared/components/field-input/field-input.component';
import { FieldSelectComponent } from '../../../shared/components/field-select/field-select.component';
import { FieldToggleComponent } from '../../../shared/components/field-toggle/field-toggle.component';
import {
  GUILDE_ECOLOGIQUE_OPTIONS,
  REPARTITION_COLONNE_EAU_OPTIONS,
  GUILDE_TROPHIQUE_OPTIONS,
  ETAT_STOCK_OPTIONS,
  STATUT_PROTECTION_OPTIONS,
  CONSERVATION_OPTIONS,
  SENSIBILITE_LUMIERE_OPTIONS,
  SENSIBILITE_COURANT_OPTIONS,
  RESISTANCE_CHOCS_OPTIONS,
  COMPORTEMENT_OPTIONS,
  FORME_CORPS_OPTIONS,
  LOCOMOTION_OPTIONS,
} from '../../../core/constants/poisson.constants';

@Component({
  selector: 'app-poissons-form',
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
  templateUrl: './poissons-form.component.html',
})
export class PoissonsFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private poissonsService = inject(PoissonsService);

  form!: FormGroup;
  isEdit = false;
  poissonId: number | null = null;
  loading = false;
  saving = false;
  activeTab: 'identite' | 'ecologie' | 'biologie' | 'nage' = 'identite';

  breadcrumbs = [
    { label: 'Poissons', route: '/poissons' },
    { label: 'Nouveau poisson' },
  ];

  guildeEcoOptions = GUILDE_ECOLOGIQUE_OPTIONS.filter(o => o.value !== '');
  repartitionOptions = REPARTITION_COLONNE_EAU_OPTIONS.filter(o => o.value !== '');
  guildeTrophiqueOptions = GUILDE_TROPHIQUE_OPTIONS.filter(o => o.value !== '');
  etatStockOptions = ETAT_STOCK_OPTIONS.filter(o => o.value !== '');
  statutProtectionOptions = STATUT_PROTECTION_OPTIONS.filter(o => o.value !== '');
  conservationOptions = CONSERVATION_OPTIONS;
  sensibiliteLumiereOptions = SENSIBILITE_LUMIERE_OPTIONS.filter(o => o.value !== '');
  sensibiliteCourantOptions = SENSIBILITE_COURANT_OPTIONS.filter(o => o.value !== '');
  resistanceOptions = RESISTANCE_CHOCS_OPTIONS.filter(o => o.value !== '');
  comportementOptions = COMPORTEMENT_OPTIONS.filter(o => o.value !== '');
  formeCorpsOptions = FORME_CORPS_OPTIONS.filter(o => o.value !== '');
  locomotionOptions = LOCOMOTION_OPTIONS.filter(o => o.value !== '');

  ngOnInit(): void {
    this.buildForm();
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEdit = true;
      this.poissonId = Number(id);
      this.loading = true;
      this.breadcrumbs[1].label = 'Modifier le poisson';
      this.poissonsService.getById(this.poissonId).subscribe({
        next: (p) => { this.form.patchValue(p); this.loading = false; },
        error: () => { this.loading = false; }
      });
    }
  }

  buildForm(): void {
    this.form = this.fb.group({
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
      interet_halieutique: [null],
      source_interet_halieutique: [''],
      etat_stock: [''],
      source_etat_stock: [''],
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
      source_resistances: [''],
      comportement: [''],
      source_comportement: [''],
      periode_reproduction: [''],
      forme_corps: [''],
      source_forme_corps: [''],
      type_peau: [''],
      source_type_peau: [''],
      locomotion: [''],
      source_locomotion: [''],
      endurance: [''],
      source_endurance: [''],
      vitesse_croisiere_juvenile_ms: [null],
      vitesse_soutenue_juvenile_ms: [null],
      vitesse_sprint_juvenile_ms: [null],
      vitesse_croisiere_adulte_ms: [null],
      vitesse_soutenue_adulte_ms: [null],
      vitesse_sprint_adulte_ms: [null],
      source_vitesse_nage: [''],
    });
  }

  setTab(tab: typeof this.activeTab): void { this.activeTab = tab; }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.saving = true;
    const data = this.form.getRawValue();
    const obs = this.isEdit && this.poissonId
      ? this.poissonsService.update(this.poissonId, data)
      : this.poissonsService.create(data);
    obs.subscribe({
      next: (p) => {
        this.saving = false;
        this.router.navigate(['/poissons', p.id_poisson]);
      },
      error: () => { this.saving = false; }
    });
  }

  onCancel(): void {
    if (this.isEdit && this.poissonId) {
      this.router.navigate(['/poissons', this.poissonId]);
    } else {
      this.router.navigate(['/poissons']);
    }
  }
}