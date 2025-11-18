import { Module } from '@nestjs/common';
import { PassportModule } from '@nestjs/passport';
import { JwtStrategy } from './jwt.strategy';
import { TestAuthController } from './test-auth.controller'; // ← Agregar esta línea

@Module({
  imports: [PassportModule.register({ defaultStrategy: 'jwt' })],
  providers: [JwtStrategy],
  controllers: [TestAuthController], // ← Agregar esta línea
  exports: [PassportModule],
})
export class AuthModule {}