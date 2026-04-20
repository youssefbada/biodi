import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { EchantillonnageService } from '../../../core/services/echantillonnage.service';
import { CentralesService } from '../../../core/services/centrales.service';
import { PoissonsService } from '../../../core/services/poissons.service';
import { NonPoissonsService } from '../../../core/services/non-poissons.service';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent } from '../../../shared/components/header/header.component';
import { SectionHeader } from '../../../shared/components/section-header/section-header';
import { FieldInputComponent } from '../../../shared/components/field-input/field-input.component';
import { FieldSelectComponent } from '../../../shared/components/field-select/field-select.component';
import { FieldToggleComponent } from '../../../shared/components/field-toggle/field-toggle.component';
import {
  GROUPE_OPTIONS,
  FREQUENCE_OCCURRENCE_OPTIONS,
} from '../../../core/constants/echantillonnage.constants';

@Component({
  selector: 'app-echantillonnage-form',
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
  templateUrl: './echantillonnage-form.component.html',
  styleUrl: './echantillonnage-form.component.scss',
})
export class EchantillonnageFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private echantillonnageService = inject(EchantillonnageService);
  private centralesService = inject(CentralesService);
  private poissonsService = inject(PoissonsService);
  private nonPoissonsService = inject(NonPoissonsService);

  form!: FormGroup;
  isEdit = false;
  itemId: number | null = null;
  loading = false;
  saving = false;
  activeTab: 'general' | 'stades' | 'saisons' = 'general';

  breadcrumbs = [
    { label: 'Échantillonnage', route: '/echantillonnage' },
    { label: 'Nouvel échantillonnage' },
  ];

  groupeOptions = GROUPE_OPTIONS.filter(o => o.value !== '');
  frequenceOptions = FREQUENCE_OCCURRENCE_OPTIONS.filter(o => o.value !== '');
  centralesOptions: { value: any; label: string }[] = [];
  poissonsOptions: { value: any; label: string }[] = [];
  nonPoissonsOptions: { value: any; label: string }[] = [];

  ngOnInit(): void {
    this.buildForm();
    this.loadOptions();
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEdit = true;
      this.itemId = Number(id);
      this.loading = true;
      this.breadcrumbs[1].label = "Modifier l'échantillonnage";
      this.echantillonnageService.getById(this.itemId).subscribe({
      next: (e) => {
        this.form.patchValue({
          ...e,
          centrale: e.centrale_id ? Number(e.centrale_id) : null,
          poisson: e.poisson_id ? Number(e.poisson_id) : null,
          non_poisson: e.non_poisson_id ? Number(e.non_poisson_id) : null,
        });
        this.loading = false;
      },
        error: () => { this.loading = false; }
      });
    }
  }

  loadOptions(): void {
    this.centralesService.getAll().subscribe(list => {
      this.centralesOptions = list.map(c => ({
        value: c.id,
        label: `${c.code_nom} — ${c.site_name}`
      }));
    });

    this.poissonsService.getAll().subscribe(list => {
      this.poissonsOptions = [
        { value: '', label: '— Aucun —' },
        ...list.map(p => ({
          value: p.id_poisson,
          label: `${p.nom_commun || ''} (${p.genre} ${p.espece})`.trim()
        }))
      ];
    });

    this.nonPoissonsService.getAll().subscribe(list => {
      this.nonPoissonsOptions = [
        { value: '', label: '— Aucun —' },
        ...list.map(p => ({
          value: p.id_non_poisson,
          label: `${p.nom_commun || ''} (${p.genre} ${p.espece})`.trim()
        }))
      ];
    });
  }

  buildForm(): void {
    this.form = this.fb.group({
      centrale: [null, Validators.required],
      date_echantillonnage: ['', Validators.required],
      nombre_echantillonnage: [null],
      duree_echantillonnage_min: [null],
      debris_vegetaux: [null],
      groupe: [''],
      poisson: [null],
      non_poisson: [null],
      frequence_occurrence: [''],
      juveniles_nombre_individus: [null],
      juveniles_pois: [null],
      juveniles_poids_moyen: [null],
      juveniles_occurence: [null],
      juveniles_pct_o: [null],
      juveniles_taille_moy_cm: [null],
      juveniles_taux_survie: [null],
      juveniles_taux_mortalite: [null],
      adultes_nombre_individus: [null],
      adultes_poids: [null],
      adultes_poids_moyen: [null],
      adultes_occurence: [null],
      adultes_pct_o: [null],
      adultes_taille_moy_cm: [null],
      adultes_taux_survie: [null],
      adultes_taux_mortalite: [null],
      totaux_nombre_individus: [null],
      totaux_poids: [null],
      totaux_poids_moyen: [null],
      totaux_occurence: [null],
      totaux_pct_o: [null],
      totaux_taille_moy: [null],
      totaux_taux_survie: [null],
      totaux_taux_mortalite: [null],
      hiver_nombre_individus: [null],
      hiver_poids: [null],
      hiver_poids_moyen: [null],
      hiver_occurence: [null],
      hiver_pct_o: [null],
      hiver_taille_moy: [null],
      hiver_taux_survie: [null],
      hiver_taux_mortalite: [null],
      hiver_nombre_echantillonnage: [''],
      printemps_nombre_individus: [null],
      printemps_poids: [null],
      printemps_poids_moyen: [null],
      printemps_occurence: [null],
      printemps_pct_o: [null],
      printemps_taille_moy: [null],
      printemps_taux_survie: [null],
      printemps_taux_mortalite: [null],
      printemps_nombre_echantillonnage: [''],
      ete_nombre_individus: [null],
      ete_poids: [null],
      ete_poids_moyen: [null],
      ete_occurence: [null],
      ete_pct_o: [null],
      ete_taille_moy: [null],
      ete_taux_survie: [null],
      ete_taux_mortalite: [null],
      ete_nombre_echantillonnage: [''],
      automne_nombre_individus: [null],
      automne_poids: [null],
      automne_poids_moyen: [null],
      automne_occurence: [null],
      automne_pct_o: [null],
      automne_taille_moy: [null],
      automne_taux_survie: [null],
      automne_taux_mortalite: [null],
      automne_nombre_echantillonnage: [''],
      sources: [''],
    });
  }

  setTab(tab: typeof this.activeTab): void { this.activeTab = tab; }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.saving = true;
    const raw = this.form.getRawValue();

    // Mapper les champs du form vers ce que le back attend
    const data = {
      ...raw,
      centrale_id: raw.centrale ? Number(raw.centrale) : null,
      poisson_id: raw.poisson ? Number(raw.poisson) : null,
      non_poisson_id: raw.non_poisson ? Number(raw.non_poisson) : null,
    };

    // Supprimer les champs incorrects
    delete data.centrale;
    delete data.poisson;
    delete data.non_poisson;

    const obs = this.isEdit && this.itemId
      ? this.echantillonnageService.update(this.itemId, data)
      : this.echantillonnageService.create(data);
    obs.subscribe({
      next: (e) => {
        this.saving = false;
        this.router.navigate(['/echantillonnage', e.id_echantillonnage]);
      },
      error: () => { this.saving = false; }
    });
  }

  onCancel(): void {
    if (this.isEdit && this.itemId) {
      this.router.navigate(['/echantillonnage', this.itemId]);
    } else {
      this.router.navigate(['/echantillonnage']);
    }
  }
}