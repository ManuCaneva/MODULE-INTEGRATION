import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { SCOPES_KEY } from './scopes.decorator';

@Injectable()
export class ScopesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredScopes = this.reflector.getAllAndOverride<string[]>(
      SCOPES_KEY,
      [context.getHandler(), context.getClass()],
    );
    
    if (!requiredScopes) {
      return true; // Si no se definen scopes, se permite el acceso
    }

    const { user } = context.switchToHttp().getRequest();
    
    // El token JWT de Keycloak pone los scopes en un string separado por espacios
    const userScopes = (user.scope || '').split(' '); 

    // Verifica si el usuario tiene al menos uno de los scopes requeridos
    return requiredScopes.some((scope) => userScopes.includes(scope));
  }
}