import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-confirm-leave-modal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './confirm-leave-modal.component.html',
  styleUrl: './confirm-leave-modal.component.scss',
})
export class ConfirmLeaveModalComponent {
  @Output() cancel = new EventEmitter<void>();
  @Output() discard = new EventEmitter<void>();
  @Output() save = new EventEmitter<void>();
}