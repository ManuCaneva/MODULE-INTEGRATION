import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService, LoginRequest } from '../../../services/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  template: `
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-4">
          <div class="card shadow">
            <div class="card-body p-4">
              <h2 class="card-title text-center mb-4">Iniciar Sesión</h2>
              
              <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    formControlName="email"
                    [class.is-invalid]="loginForm.get('email')?.invalid && loginForm.get('email')?.touched"
                    placeholder="tu@email.com"
                  >
                  <div class="invalid-feedback" *ngIf="loginForm.get('email')?.errors?.['required']">
                    El email es requerido
                  </div>
                  <div class="invalid-feedback" *ngIf="loginForm.get('email')?.errors?.['email']">
                    Formato de email inválido
                  </div>
                </div>

                <div class="mb-3">
                  <label for="password" class="form-label">Contraseña</label>
                  <input
                    type="password"
                    class="form-control"
                    id="password"
                    formControlName="password"
                    [class.is-invalid]="loginForm.get('password')?.invalid && loginForm.get('password')?.touched"
                    placeholder="Tu contraseña"
                  >
                  <div class="invalid-feedback" *ngIf="loginForm.get('password')?.errors?.['required']">
                    La contraseña es requerida
                  </div>
                  <div class="invalid-feedback" *ngIf="loginForm.get('password')?.errors?.['minlength']">
                    Mínimo 6 caracteres
                  </div>
                </div>

                <div class="d-grid gap-2">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    [disabled]="loginForm.invalid || loading"
                  >
                    <span *ngIf="loading" class="spinner-border spinner-border-sm me-2"></span>
                    {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
                  </button>
                </div>

                <div class="text-center mt-3">
                  <a routerLink="/register" class="text-decoration-none">¿No tienes cuenta? Regístrate</a>
                </div>
              </form>

              <div *ngIf="errorMessage" class="alert alert-danger mt-3" role="alert">
                {{ errorMessage }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class LoginComponent {
  loginForm: FormGroup;
  loading = false;
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      this.loading = true;
      this.errorMessage = '';

      const credentials: LoginRequest = this.loginForm.value;

      this.authService.login(credentials).subscribe({
        next: (response: string) => {
          this.loading = false;
          if (response.includes('exitoso')) {
            this.router.navigate(['/dashboard']);
          } else {
            this.errorMessage = response;
          }
        },
        error: (error: any) => {
          this.loading = false;
          // Manejar diferentes tipos de errores HTTP
          if (error.status === 401) {
            this.errorMessage = 'Credenciales inválidas';
          } else if (error.status === 400) {
            this.errorMessage = 'Datos inválidos';
          } else {
            this.errorMessage = 'Error del servidor. Intenta nuevamente.';
          }
          console.error('Login error:', error);
        }
      });
    }
  }
}