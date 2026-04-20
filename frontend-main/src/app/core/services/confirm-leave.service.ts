import { Injectable, signal } from '@angular/core';
import { Subject, firstValueFrom } from 'rxjs';
import { CanComponentDeactivate } from '../guards/confirm-leave.guard';

@Injectable({
  providedIn: 'root',
})
export class ConfirmLeaveService {

  // Signal pour afficher/cacher la modal
  showModal = signal<boolean>(false);

  private response$ = new Subject<'cancel' | 'discard' | 'save'>();
  private currentComponent: CanComponentDeactivate | null = null;

  askConfirmation(component: CanComponentDeactivate): Promise<boolean> {
    this.currentComponent = component;
    this.showModal.set(true);

    return firstValueFrom(this.response$).then(response => {
      this.showModal.set(false);
      if (response === 'discard') return true;
      if (response === 'save') {
        component.saveEdit();
        return true;
      }
      return false; // cancel
    });
  }

  respond(action: 'cancel' | 'discard' | 'save'): void {
    this.response$.next(action);
  }
}