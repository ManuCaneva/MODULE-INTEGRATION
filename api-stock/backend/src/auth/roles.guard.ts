import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { ROLES_KEY } from './roles.decorator';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    // 1. Get roles required by the @Roles decorator
    const requiredRoles = this.reflector.getAllAndOverride<string[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    // 2. If no roles are required, allow access
    if (!requiredRoles) {
      return true;
    }

    // 3. Get the user object attached by JwtAuthGuard
    const { user } = context.switchToHttp().getRequest();

    // 4. Extract user's roles from the token payload
    // IMPORTANT: Adjust this path based on where roles are in YOUR token!
    const userRoles = user?.realm_access?.roles || user?.roles || []; 

    // 5. Check if the user has at least one of the required roles
    return requiredRoles.some((role) => userRoles.includes(role));
  }
}