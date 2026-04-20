import {
  Component,
  Input,
  Output,
  EventEmitter,
  inject,
  signal,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImportService, ImportResult } from '../../../core/services/import.service';

export interface ColumnMapping {
  excelHeader: string;    // nom colonne dans le fichier Excel
  modelField: string;     // nom champ dans le modèle Angular
  label: string;          // label affiché à l'utilisateur
  required: boolean;      // champ obligatoire ?
}

export type ImportStatus = 'idle' | 'reading' | 'validating' | 'importing' | 'done' | 'error';

export interface ValidationError {
  ligne: number;
  champ: string;
  message: string;
}

@Component({
  selector: 'app-import-modal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './import-modal.component.html',
  styleUrl: './import-modal.component.scss',
})
export class ImportModalComponent {

  private importService = inject(ImportService);

  // ─── Inputs ───
  @Input() title: string = 'Importer des données (Excel)';
  @Input() columnMappings: ColumnMapping[] = [];
  @Input() createFn!: (row: any) => any;

  // ─── Outputs ───
  @Output() closed = new EventEmitter<void>();
  @Output() importDone = new EventEmitter<ImportResult>();

  // ─── State ───
  status = signal<ImportStatus>('idle');
  selectedFile = signal<File | null>(null);
  validationErrors = signal<ValidationError[]>([]);
  progress = signal<number>(0);
  progressLabel = signal<string>('');
  result = signal<ImportResult | null>(null);
  isDragging = signal<boolean>(false);

  // ─── Drag & Drop ───
  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragging.set(true);
  }

  onDragLeave(): void {
    this.isDragging.set(false);
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragging.set(false);
    const file = event.dataTransfer?.files[0];
    if (file) this.handleFile(file);
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) this.handleFile(input.files[0]);
  }

  // ─── Handle file ───
  async handleFile(file: File): Promise<void> {
    const validation = this.importService.validateFile(file);
    if (!validation.valid) {
      this.status.set('error');
      this.progressLabel.set(validation.error || 'Fichier invalide');
      return;
    }

    this.selectedFile.set(file);
    this.status.set('reading');
    this.progress.set(20);
    this.progressLabel.set('Lecture du fichier...');

    try {
      const rows = await this.importService.readFile(file);

      this.status.set('validating');
      this.progress.set(50);
      this.progressLabel.set('Vérification de la conformité des données...');

      const errors = this.validateRows(rows);
      this.validationErrors.set(errors);

      if (errors.length === 0) {
        this.progress.set(100);
        this.progressLabel.set(`${rows.length} ligne(s) prête(s) à importer`);
        this.status.set('done');
      } else {
        this.progress.set(100);
        this.progressLabel.set(`${errors.length} erreur(s) détectée(s)`);
        this.status.set('error');
      }
    } catch (err) {
      this.status.set('error');
      this.progressLabel.set('Erreur lors de la lecture du fichier');
    }
  }

  // ─── Validation conformité ───
  validateRows(rows: any[]): ValidationError[] {
    const errors: ValidationError[] = [];

    if (rows.length === 0) {
      errors.push({ ligne: 0, champ: '', message: 'Le fichier est vide' });
      return errors;
    }

    // Vérifie colonnes obligatoires
    const requiredMappings = this.columnMappings.filter(m => m.required);

    rows.forEach((row, index) => {
      requiredMappings.forEach(mapping => {
        const value = row[mapping.excelHeader];
        if (value === null || value === undefined || value === '') {
          errors.push({
            ligne: index + 2,
            champ: mapping.label,
            message: `Champ obligatoire manquant : "${mapping.label}"`,
          });
        }
      });
    });

    return errors;
  }

  // ─── Import ───
  async onImport(): Promise<void> {
    if (!this.selectedFile()) return;

    this.status.set('importing');
    this.progress.set(0);
    this.progressLabel.set('Import en cours...');

    try {
      const rows = await this.importService.readFile(this.selectedFile()!);
      const mappedRows = this.mapRows(rows);

      this.importService.importRows(mappedRows, this.createFn).subscribe({
        next: (result) => {
          this.result.set(result);
          this.progress.set(100);
          this.progressLabel.set(
            `${result.success}/${result.total} ligne(s) importée(s) avec succès`
          );
          this.status.set('done');
          this.importDone.emit(result);
        },
        error: () => {
          this.status.set('error');
          this.progressLabel.set('Erreur lors de l\'import');
        },
      });
    } catch {
      this.status.set('error');
      this.progressLabel.set('Erreur lors de la lecture');
    }
  }

  // ─── Mapping Excel → modèle ───
  mapRows(rows: any[]): any[] {
    return rows.map(row => {
      const mapped: any = {};
      this.columnMappings.forEach(m => {
        mapped[m.modelField] = row[m.excelHeader] ?? null;
      });
      return mapped;
    });
  }

  // ─── Reset ───
  reset(): void {
    this.status.set('idle');
    this.selectedFile.set(null);
    this.validationErrors.set([]);
    this.progress.set(0);
    this.progressLabel.set('');
    this.result.set(null);
  }

  onClose(): void {
    this.reset();
    this.closed.emit();
  }

  get canImport(): boolean {
    return this.status() === 'done' && this.validationErrors().length === 0 && !!this.selectedFile();
  }

  get progressPercent(): number {
    return this.progress();
  }
}