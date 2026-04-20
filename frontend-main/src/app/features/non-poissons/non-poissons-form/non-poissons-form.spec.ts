import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NonPoissonsFormComponent } from './non-poissons-form.component';

describe('NonPoissonsForm', () => {
  let component: NonPoissonsFormComponent;
  let fixture: ComponentFixture<NonPoissonsFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NonPoissonsFormComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NonPoissonsFormComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
