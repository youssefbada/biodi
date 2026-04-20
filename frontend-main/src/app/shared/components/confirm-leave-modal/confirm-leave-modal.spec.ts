import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConfirmLeaveModal } from './confirm-leave-modal';

describe('ConfirmLeaveModal', () => {
  let component: ConfirmLeaveModal;
  let fixture: ComponentFixture<ConfirmLeaveModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConfirmLeaveModal]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConfirmLeaveModal);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
