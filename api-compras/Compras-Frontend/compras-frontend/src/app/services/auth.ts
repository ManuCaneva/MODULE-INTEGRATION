import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  repeatPassword: string;
  firstName: string;
  lastName: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  
  private apiUrl = 'https://localhost:7248/api';

  constructor(private http: HttpClient) { }

  login(credentials: LoginRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/login`, credentials, { 
      responseType: 'text'
    }).pipe(
      tap((response: string) => {
        if (response.includes('exitoso')) {
          localStorage.setItem('isLoggedIn', 'true');
          localStorage.setItem('userEmail', credentials.email);
        }
      })
    );
  }

  register(userData: RegisterRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/register`, userData, {
      responseType: 'text'
    });
  }

  logout(): void {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userEmail');
  }

  isLoggedIn(): boolean {
    return localStorage.getItem('isLoggedIn') === 'true';
  }

  getCurrentUserEmail(): string | null {
    return localStorage.getItem('userEmail');
  }
}