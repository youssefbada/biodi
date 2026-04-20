import { CanDeactivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { ConfirmLeaveService } from '../services/confirm-leave.service';

export interface CanComponentDeactivate {
  isEditing: () => boolean;
  saveEdit: () => void;
}

export const confirmLeaveGuard: CanDeactivateFn<CanComponentDeactivate> = (component) => {
  if (!component.isEditing()) return true;

  const service = inject(ConfirmLeaveService);
  return service.askConfirmation(component);
};