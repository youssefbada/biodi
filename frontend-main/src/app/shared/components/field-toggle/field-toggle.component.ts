// src/app/shared/components/field-toggle/field-toggle.component.ts
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';

@Component({
  selector: 'app-field-toggle',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './field-toggle.component.html',
  styleUrl: './field-toggle.component.scss'
})
export class FieldToggleComponent {
  @Input() label = '';
  @Input() controlName = '';
  @Input() formGroup!: FormGroup;
  @Input() editing = false;
  @Input() description = '';
  @Input() serverError = '';

  get control(): FormControl {
    return this.formGroup?.get(this.controlName) as FormControl;
  }

  get currentValue(): boolean | null {
    return this.formGroup?.get(this.controlName)?.value ?? null;
  }
}
