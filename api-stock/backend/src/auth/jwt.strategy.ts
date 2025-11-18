import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { passportJwtSecret } from 'jwks-rsa';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    // --- INICIO DE LA CORRECCIÓN ---
    // 1. Obtener la variable de entorno
    const jwksUri = process.env.KEYCLOAK_JWKS_URI;

    // 2. Verificar que la variable existe
    if (!jwksUri) {
      throw new Error('La variable de entorno KEYCLOAK_JWKS_URI no está definida.');
    }
    // --- FIN DE LA CORRECCIÓN ---

    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      issuer: process.env.KEYCLOAK_ISSUER_URL,
      algorithms: ['RS256'],

      secretOrKeyProvider: passportJwtSecret({
        cache: true,
        rateLimit: true,
        jwksRequestsPerMinute: 5,
        jwksUri: jwksUri, // <-- 3. Usar la variable verificada (ahora es 100% string)
      }),
    });
  }

  async validate(payload: any) {
    // Lo que retornes aquí se adjuntará a request.user
    return payload;
  }
}