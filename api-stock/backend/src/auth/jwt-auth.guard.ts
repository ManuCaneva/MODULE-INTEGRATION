// jwt-auth.guard.ts (modificado)
import { Injectable, ExecutionContext, UnauthorizedException } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { Observable } from 'rxjs';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  canActivate(context: ExecutionContext): boolean | Promise<boolean> | Observable<boolean> {
    const request = context.switchToHttp().getRequest();
    console.log('🔐 JwtAuthGuard - Headers:', request.headers);
    console.log('🔐 JwtAuthGuard - Authorization header:', request.headers.authorization);
    
    return super.canActivate(context);
  }

  handleRequest(err: any, user: any, info: any) {
    console.log('🔐 JwtAuthGuard - handleRequest - User:', user);
    console.log('🔐 JwtAuthGuard - handleRequest - Error:', err);
    console.log('🔐 JwtAuthGuard - handleRequest - Info:', info);
    
    if (err || !user) {
      console.log('🔐 JwtAuthGuard - ACCESO DENEGADO');
      throw new UnauthorizedException('Token inválido o no proporcionado');
    }
    return user;
  }
}