import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { EchantillonnageService } from '../../../core/services/echantillonnage.service';
import { CentralesService } from '../../../core/services/centrales.service';
import { PoissonsService } from '../../../core/services/poissons.service';
import { NonPoissonsService } from '../../../core/services/non-poissons.service';
import { Echantillonnage } from '../../../models/echantillonnage.model';
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
  FREQUENCE_OCCURRENCE_OPTIONS,
} from '../../../core/constants/echantillonnage.constants';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-echantillonnage-detail',
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
  templateUrl: './echantillonnage-detail.component.html',
  styleUrl: './echantillonnage-detail.component.scss',
})
export class EchantillonnageDetailComponent implements OnInit, CanComponentDeactivate {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private fb = inject(FormBuilder);
  private echantillonnageService = inject(EchantillonnageService);
  private centralesService = inject(CentralesService);
  private poissonsService = inject(PoissonsService);
  private nonPoissonsService = inject(NonPoissonsService);
  authService = inject(AuthService);
  confirmLeaveService = inject(ConfirmLeaveService);

  item: Echantillonnage | null = null;
  loading = true;
  error = false;
  editing = false;
  saving = false;
  saved = false;
  activeTab: 'general' | 'stades' | 'saisons' = 'general';

  form!: FormGroup;

  breadcrumbs = [
    { label: 'Échantillonnage', route: '/echantillonnage' },
    { label: 'Fiche détail' },
  ];

  groupeOptions = GROUPE_OPTIONS.filter(o => o.value !== '');
  frequenceOptions = FREQUENCE_OCCURRENCE_OPTIONS.filter(o => o.value !== '');
  centralesOptions: { value: any; label: string }[] = [];
  poissonsOptions: { value: any; label: string }[] = [];
  nonPoissonsOptions: { value: any; label: string }[] = [];

  isEditing(): boolean { return this.editing; }


ngOnInit(): void {
  this.buildForm();
  const id = Number(this.route.snapshot.paramMap.get('id'));

  // Charger les options ET les données en parallèle
  forkJoin({
    item: this.echantillonnageService.getById(id),
    centrales: this.centralesService.getAll(),
    poissons: this.poissonsService.getAll(),
    nonPoissons: this.nonPoissonsService.getAll(),
  }).subscribe({
    next: ({ item, centrales, poissons, nonPoissons }) => {
      // Remplir les options d'abord
      this.centralesOptions = centrales.map(c => ({
        value: Number(c.id),
        label: `${c.code_nom} — ${c.site_name}`
      }));

      this.poissonsOptions = [
        { value: '', label: '— Aucun —' },
        ...poissons.map(p => ({
          value: p.id_poisson,
          label: `${p.nom_commun || ''} (${p.genre} ${p.espece})`.trim()
        }))
      ];

      this.nonPoissonsOptions = [
        { value: '', label: '— Aucun —' },
        ...nonPoissons.map(p => ({
          value: p.id_non_poisson,
          label: `${p.nom_commun || ''} (${p.genre} ${p.espece})`.trim()
        }))
      ];

      // Puis patcher le form
     this.item = item;
      this.form.patchValue({
        ...item,
        centrale: item.centrale_id ? Number(item.centrale_id) : null,
        poisson: item.poisson_id ? Number(item.poisson_id) : null,
        non_poisson: item.non_poisson_id ? Number(item.non_poisson_id) : null,
      });
      this.breadcrumbs[1].label = `Fiche ${item.id_echantillonnage}`;
      this.loading = false;
    },
    error: () => { this.error = true; this.loading = false; }
  });
}


  // loadOptions(): void {
  //   this.centralesService.getAll().subscribe(list => {
  //     this.centralesOptions = list.map(c => ({
  //       value: c.id,
  //       label: `${c.code_nom} — ${c.site_name}`
  //     }));
  //   });

  //   this.poissonsService.getAll().subscribe(list => {
  //     this.poissonsOptions = [
  //       { value: '', label: '— Aucun —' },
  //       ...list.map(p => ({
  //         value: p.id_poisson,
  //         label: `${p.nom_commun || ''} (${p.genre} ${p.espece})`.trim()
  //       }))
  //     ];
  //   });

  //   this.nonPoissonsService.getAll().subscribe(list => {
  //     this.nonPoissonsOptions = [
  //       { value: '', label: '— Aucun —' },
  //       ...list.map(p => ({
  //         value: p.id_non_poisson,
  //         label: `${p.nom_commun || ''} (${p.genre} ${p.espece})`.trim()
  //       }))
  //     ];
  //   });
  // }

  buildForm(): void {
    this.form = this.fb.group({
      centrale: [null],
      date_echantillonnage: [''],
      nombre_echantillonnage: [null],
      duree_echantillonnage_min: [null],
      debris_vegetaux: [null],
      groupe: [''],
      poisson: [null],
      non_poisson: [null],
      frequence_occurrence: [''],
      // Juvéniles
      juveniles_nombre_individus: [null],
      juveniles_pois: [null],
      juveniles_poids_moyen: [null],
      juveniles_occurence: [null],
      juveniles_pct_o: [null],
      juveniles_taille_moy_cm: [null],
      juveniles_taux_survie: [null],
      juveniles_taux_mortalite: [null],
      // Adultes
      adultes_nombre_individus: [null],
      adultes_poids: [null],
      adultes_poids_moyen: [null],
      adultes_occurence: [null],
      adultes_pct_o: [null],
      adultes_taille_moy_cm: [null],
      adultes_taux_survie: [null],
      adultes_taux_mortalite: [null],
      // Totaux
      totaux_nombre_individus: [null],
      totaux_poids: [null],
      totaux_poids_moyen: [null],
      totaux_occurence: [null],
      totaux_pct_o: [null],
      totaux_taille_moy: [null],
      totaux_taux_survie: [null],
      totaux_taux_mortalite: [null],
      // Saisons
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
  const id = this.item.id_echantillonnage;
  if (id === undefined) return;

  const raw = this.form.getRawValue();
  const data = {
    ...raw,
    centrale_id: raw.centrale ? Number(raw.centrale) : null,
    poisson_id: raw.poisson ? Number(raw.poisson) : null,
    non_poisson_id: raw.non_poisson ? Number(raw.non_poisson) : null,
  };
  delete data.centrale;
  delete data.poisson;
  delete data.non_poisson;

  this.echantillonnageService.update(id, data).subscribe({
    next: (updated) => {
      this.item = updated;
      this.form.patchValue({
        ...updated,
        centrale: updated.centrale_id ? Number(updated.centrale_id) : null,
        poisson: updated.poisson_id ? Number(updated.poisson_id) : null,
        non_poisson: updated.non_poisson_id ? Number(updated.non_poisson_id) : null,
      });
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

  goBack(): void { this.router.navigate(['/echantillonnage']); }
}