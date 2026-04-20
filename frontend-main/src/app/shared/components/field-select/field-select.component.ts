// src/app/shared/components/field-select/field-select.component.ts
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';

export interface SelectOption {
  value: string;
  label: string;
}

@Component({
  selector: 'app-field-select',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './field-select.component.html',
  styleUrl: './field-select.component.scss'
})
export class FieldSelectComponent {
  @Input() label = '';
  @Input() controlName = '';
  @Input() formGroup!: FormGroup;
  @Input() editing = false;
  @Input() options: SelectOption[] = [];
  @Input() required = false;
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
    return 'Champ invalide';
  }

  get displayValue(): string {
    const val = this.formGroup?.get(this.controlName)?.value;
    if (val === null || val === undefined || val === '') return '—';
    const found = this.options.find(o => o.value === val);
    return found ? found.label : String(val);
  }
}
