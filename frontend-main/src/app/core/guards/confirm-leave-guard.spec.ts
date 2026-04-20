import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { confirmLeaveGuard } from './confirm-leave.guard';

describe('confirmLeaveGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) =>
      TestBed.runInInjectionContext(() => confirmLeaveGuard(...guardParameters));

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
