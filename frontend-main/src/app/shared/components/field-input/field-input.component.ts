// src/app/shared/components/field-input/field-input.component.ts
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, AbstractControl, FormControl } from '@angular/forms';

@Component({
  selector: 'app-field-input',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './field-input.component.html',
  styleUrl: './field-input.component.scss'
})
export class FieldInputComponent {
  @Input() label = '';
  @Input() controlName = '';
  @Input() formGroup!: FormGroup;
  @Input() editing = false;
  @Input() type: 'text' | 'number' | 'textarea' = 'text';
  @Input() placeholder = '';
  @Input() unit = '';
  @Input() required = false;
  @Input() rows = 4;
  @Input() serverError = '';

  get control(): FormControl {
    return this.formGroup?.get(this.controlName) as FormControl;
  }

  get showError(): boolean {
    if (!this.editing || !this.control) return false;
    if (this.serverError) return true;
    return this.control.invalid && (this.control.touched || this.control.dirty);
  }

  get errorMessage(): string {
    if (this.serverError) return this.serverError;
    if (!this.control || !this.control.errors) return '';
    if (this.control.errors['required']) return `${this.label} est obligatoire`;
    if (this.control.errors['min']) return `La valeur minimale est ${this.control.errors['min'].min}`;
    if (this.control.errors['max']) return `La valeur maximale est ${this.control.errors['max'].max}`;
    return 'Champ invalide';
  }

  get displayValue(): string {
    const val = this.formGroup?.get(this.controlName)?.value;
    if (val === null || val === undefined || val === '') return '—';
    return this.unit ? `${val} ${this.unit}` : String(val);
  }
}
