import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { forkJoin } from 'rxjs';
import { InventaireService } from '../../../core/services/inventaire.service';
import { CentralesService } from '../../../core/services/centrales.service';
import { PoissonsService } from '../../../core/services/poissons.service';
import { NonPoissonsService } from '../../../core/services/non-poissons.service';
import { Inventaire } from '../../../models/inventaire.model';
import { AuthService } from '../../../core/services/auth.service';
import { ConfirmLeaveService } from '../../../core/services/confirm-leave.service';
import { CanComponentDeactivate } from '../../../core/guards/confirm-leave.guard';
import { SidebarComponent } from '../../../shared/components/sidebar/sidebar.component';
import { HeaderComponent } from '../../../shared/components/header/header.component';
import { SectionHeader } from '../../../shared/components/section-header/section-header';
import { FieldInputComponent } from '../../../shared/components/field-input/field-input.component';
import { FieldSelectComponent } from '../../../shared/components/field-select/field-select.component';
import { ConfirmLeaveModalComponent } from '../../../shared/components/confirm-leave-modal/confirm-leave-modal.component';
import { GROUPE_OPTIONS } from '../../../core/constants/non-poisson.constants';

@Component({
  selector: 'app-inventaire-detail',
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
    ConfirmLeaveModalComponent,
  ],
  templateUrl: './inventaire-detail.component.html',
  styleUrl: './inventaire-detail.component.scss',
})
export class InventaireDetailComponent implements OnInit, CanComponentDeactivate {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private fb = inject(FormBuilder);
  private inventaireService = inject(InventaireService);
  private centralesService = inject(CentralesService);
  private poissonsService = inject(PoissonsService);
  private nonPoissonsService = inject(NonPoissonsService);
  authService = inject(AuthService);
  confirmLeaveService = inject(ConfirmLeaveService);

  item: Inventaire | null = null;
  loading = true;
  error = false;
  editing = false;
  saving = false;
  saved = false;

  form!: FormGroup;

  breadcrumbs = [
    { label: 'Inventaire', route: '/inventaire' },
    { label: 'Fiche détail' },
  ];

  groupeOptions = GROUPE_OPTIONS.filter(o => o.value !== '');
  centralesOptions: { value: any; label: string }[] = [];
  poissonsOptions: { value: any; label: string }[] = [];
  nonPoissonsOptions: { value: any; label: string }[] = [];

  isEditing(): boolean { return this.editing; }

  ngOnInit(): void {
    this.buildForm();
    const id = Number(this.route.snapshot.paramMap.get('id'));

    forkJoin({
      item: this.inventaireService.getById(id),
      centrales: this.centralesService.getAll(),
      poissons: this.poissonsService.getAll(),
      nonPoissons: this.nonPoissonsService.getAll(),
    }).subscribe({
      next: ({ item, centrales, poissons, nonPoissons }) => {
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

        this.item = item;
        this.form.patchValue({
          ...item,
          centrale: item.centrale_id ? Number(item.centrale_id) : null,
          espece_poisson: item.espece_poisson_id ? Number(item.espece_poisson_id) : null,
          espece_non_poisson: item.espece_non_poisson_id ? Number(item.espece_non_poisson_id) : null,
        });
        this.breadcrumbs[1].label = `Inventaire ${item.id_inventaire}`;
        this.loading = false;
      },
      error: () => { this.error = true; this.loading = false; }
    });
  }
  get hasPoisson(): boolean {
      return !!this.form.get('espece_poisson')?.value;
    }

  get hasNonPoisson(): boolean {
    return !!this.form.get('espece_non_poisson')?.value;
  }
  buildForm(): void {
    this.form = this.fb.group({
      centrale: [null],
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

  startEdit(): void {
    if (!this.item) return;
    this.form.patchValue({
      ...this.item,
      centrale: this.item.centrale_id ? Number(this.item.centrale_id) : null,
      espece_poisson: this.item.espece_poisson_id ? Number(this.item.espece_poisson_id) : null,
      espece_non_poisson: this.item.espece_non_poisson_id ? Number(this.item.espece_non_poisson_id) : null,
    });
    this.editing = true;
    this.saved = false;
  }

  cancelEdit(): void {
    this.editing = false;
    if (this.item) {
      this.form.patchValue({
        ...this.item,
        centrale: this.item.centrale_id ? Number(this.item.centrale_id) : null,
        espece_poisson: this.item.espece_poisson_id ? Number(this.item.espece_poisson_id) : null,
        espece_non_poisson: this.item.espece_non_poisson_id ? Number(this.item.espece_non_poisson_id) : null,
      });
    }
  }

  saveEdit(): void {
    if (!this.item || this.form.invalid) return;
    this.saving = true;
    const id = this.item.id_inventaire;
    if (id === undefined) return;

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

    this.inventaireService.update(id, data).subscribe({
      next: (updated) => {
        this.item = updated;
        this.form.patchValue({
          ...updated,
          centrale: updated.centrale_id ? Number(updated.centrale_id) : null,
          espece_poisson: updated.espece_poisson_id ? Number(updated.espece_poisson_id) : null,
          espece_non_poisson: updated.espece_non_poisson_id ? Number(updated.espece_non_poisson_id) : null,
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

  goBack(): void { this.router.navigate(['/inventaire']); }
}