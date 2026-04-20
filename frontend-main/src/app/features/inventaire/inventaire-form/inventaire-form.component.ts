import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { forkJoin } from 'rxjs';
import { InventaireService } from '../../../core/services/inventaire.service';
import { CentralesService } from '../../../core/services/centrales.service';
import { PoissonsService } from '../../../core/services/poissons.service';
import { NonPoissonsService } from '../../../core/services/non-poissons.service';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent } from '../../../shared/components/header/header.component';
import { SectionHeader } from '../../../shared/components/section-header/section-header';
import { FieldInputComponent } from '../../../shared/components/field-input/field-input.component';
import { FieldSelectComponent } from '../../../shared/components/field-select/field-select.component';
import { GROUPE_OPTIONS } from '../../../core/constants/non-poisson.constants';

@Component({
  selector: 'app-inventaire-form',
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
  ],
  templateUrl: './inventaire-form.component.html',
  styleUrl: './inventaire-form.component.scss',
})
export class InventaireFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private inventaireService = inject(InventaireService);
  private centralesService = inject(CentralesService);
  private poissonsService = inject(PoissonsService);
  private nonPoissonsService = inject(NonPoissonsService);

  form!: FormGroup;
  isEdit = false;
  itemId: number | null = null;
  loading = false;
  saving = false;

  breadcrumbs = [
    { label: 'Inventaire', route: '/inventaire' },
    { label: 'Nouvel inventaire' },
  ];

  groupeOptions = GROUPE_OPTIONS.filter(o => o.value !== '');
  centralesOptions: { value: any; label: string }[] = [];
  poissonsOptions: { value: any; label: string }[] = [];
  nonPoissonsOptions: { value: any; label: string }[] = [];

  ngOnInit(): void {
    this.buildForm();
    const id = this.route.snapshot.paramMap.get('id');

    if (id) {
      this.isEdit = true;
      this.itemId = Number(id);
      this.loading = true;
      this.breadcrumbs[1].label = "Modifier l'inventaire";

      forkJoin({
        item: this.inventaireService.getById(this.itemId),
        centrales: this.centralesService.getAll(),
        poissons: this.poissonsService.getAll(),
        nonPoissons: this.nonPoissonsService.getAll(),
      }).subscribe({
        next: ({ item, centrales, poissons, nonPoissons }) => {
          this.loadOptionsFromData(centrales, poissons, nonPoissons);
          this.form.patchValue({
            ...item,
            centrale: item.centrale_id ? Number(item.centrale_id) : null,
            espece_poisson: item.espece_poisson_id ? Number(item.espece_poisson_id) : null,
            espece_non_poisson: item.espece_non_poisson_id ? Number(item.espece_non_poisson_id) : null,
          });
          this.loading = false;
        },
        error: () => { this.loading = false; }
      });
    } else {
      forkJoin({
        centrales: this.centralesService.getAll(),
        poissons: this.poissonsService.getAll(),
        nonPoissons: this.nonPoissonsService.getAll(),
      }).subscribe({
        next: ({ centrales, poissons, nonPoissons }) => {
          this.loadOptionsFromData(centrales, poissons, nonPoissons);
        }
      });
    }
  }
  get hasPoisson(): boolean {
    return !!this.form.get('espece_poisson')?.value;
  }

  get hasNonPoisson(): boolean {
    return !!this.form.get('espece_non_poisson')?.value;
  }
  loadOptionsFromData(centrales: any[], poissons: any[], nonPoissons: any[]): void {
    this.centralesOptions = centrales.map(c => ({
      value: Number(c.id),
      label: `${c.code_nom} — ${c.site_name}`
    }));

    this.poissonsOptions = [
      { value: '', label: '— Aucun —' },
      ...poissons.map(p => ({
        value: Number(p.id_poisson),
        label: `${p.nom_commun || ''} (${p.genre} ${p.espece})`.trim()
      }))
    ];

    this.nonPoissonsOptions = [
      { value: '', label: '— Aucun —' },
      ...nonPoissons.map(p => ({
        value: Number(p.id_non_poisson),
        label: `${p.nom_commun || ''} (${p.genre} ${p.espece})`.trim()
      }))
    ];
  }

  buildForm(): void {
    this.form = this.fb.group({
      centrale: [null, Validators.required],
      espece_poisson: [null],
      espece_non_poisson: [null],
      nom_commun: [''],
      groupe_poisson: [''],
      groupe_non_poisson: [''],
    });

      // Quand poisson sélectionné → vider non-poisson
      this.form.get('espece_poisson')?.valueChanges.subscribe(val => {
        if (val) {
          this.form.get('espece_non_poisson')?.setValue(null, { emitEvent: false });
          this.form.get('groupe_non_poisson')?.setValue('', { emitEvent: false });
        }
      });

      // Quand non-poisson sélectionné → vider poisson
      this.form.get('espece_non_poisson')?.valueChanges.subscribe(val => {
        if (val) {
          this.form.get('espece_poisson')?.setValue(null, { emitEvent: false });
          this.form.get('groupe_poisson')?.setValue('', { emitEvent: false });
        }
      });
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.saving = true;
    const raw = this.form.getRawValue();
    const data = {
      ...raw,
      centrale_id: raw.centrale ? Number(raw.centrale) : null,
      espece_poisson_id: raw.espece_poisson ? Number(raw.espece_poisson) : null,
      espece_non_poisson_id: raw.espece_non_poisson ? Number(raw.espece_non_poisson) : null,
    };
    delete data.centrale;
    delete data.espece_poisson;
    delete data.espece_non_poisson;

    const obs = this.isEdit && this.itemId
      ? this.inventaireService.update(this.itemId, data)
      : this.inventaireService.create(data);

    obs.subscribe({
      next: (i) => {
        this.saving = false;
        this.router.navigate(['/inventaire', i.id_inventaire]);
      },
      error: () => { this.saving = false; }
    });
  }

  onCancel(): void {
    if (this.isEdit && this.itemId) {
      this.router.navigate(['/inventaire', this.itemId]);
    } else {
      this.router.navigate(['/inventaire']);
    }
  }
}