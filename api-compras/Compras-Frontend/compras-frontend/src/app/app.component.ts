import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink],
  template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <a class="navbar-brand" routerLink="/dashboard">Compras App</a>
        <div class="navbar-nav ms-auto">
          <a class="nav-link" routerLink="/login">Login</a>
          <a class="nav-link" routerLink="/register">Register</a>
        </div>
      </div>
    </nav>
    
    <main>
      <router-outlet></router-outlet>
    </main>
  `,
  styles: [`
    main { min-height: calc(100vh - 56px); }
  `]
})
export class AppComponent {
  title = 'compras-frontend';
}