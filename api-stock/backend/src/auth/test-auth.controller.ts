import { Controller, Get, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { ScopesGuard } from '../auth/scopes.guard';
import { Scopes } from '../auth/scopes.decorator';

@Controller('test-auth')
export class TestAuthController {
  
  @Get('public')
  publicEndpoint() {
    console.log('✅ test-auth/public accessed');
    return { 
      message: 'Este endpoint es público - FUNCIONA!', 
      timestamp: new Date().toISOString(),
      status: 'OK'
    };
  }

  @Get('jwt-only')
  @UseGuards(JwtAuthGuard)
  jwtOnlyEndpoint() {
    return { 
      message: 'Solo JWT requerido - ACCESO CONCEDIDO', 
      timestamp: new Date().toISOString()
    };
  }

  @Get('jwt-and-scopes')
  @UseGuards(JwtAuthGuard, ScopesGuard)
  @Scopes('productos:read')
  jwtAndScopesEndpoint() {
    return { 
      message: 'JWT + Scopes requeridos - ACCESO CONCEDIDO', 
      timestamp: new Date().toISOString()
    };
  }
}