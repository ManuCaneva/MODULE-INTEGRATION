import NextAuth, { NextAuthOptions, Session, Account, User } from "next-auth"
import { JWT } from "next-auth/jwt"
import KeycloakProvider from "next-auth/providers/keycloak"
import jwt from "jsonwebtoken";

interface DecodedToken {
  realm_access?: {
    roles?: string[];
  };
  exp?: number;
}

// Extender el tipo JWT para incluir nuestros campos personalizados
interface ExtendedJWT extends JWT {
  accessToken?: string;
  refreshToken?: string;
  accessTokenExpires?: number;
  roles?: string[];
  error?: string;
}

// Extender el tipo Session para incluir nuestros campos personalizados
interface ExtendedSession extends Session {
  accessToken?: string;
  roles?: string[];
  error?: string;
}

async function refreshAccessToken(token: ExtendedJWT): Promise<ExtendedJWT> {
  try {
    const url = `${process.env.KEYCLOAK_ISSUER}/protocol/openid-connect/token`;

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        client_id: process.env.KEYCLOAK_CLIENT_ID!,
        client_secret: process.env.KEYCLOAK_CLIENT_SECRET!,
        grant_type: "refresh_token",
        refresh_token: token.refreshToken!,
      }),
    });

    const refreshedTokens = await response.json();

    if (!response.ok) {
      throw refreshedTokens;
    }

    const decodedToken: DecodedToken | null = jwt.decode(refreshedTokens.access_token) as DecodedToken | null;

    return {
      ...token,
      accessToken: refreshedTokens.access_token,
      accessTokenExpires: Date.now() + (refreshedTokens.expires_in * 1000),
      refreshToken: refreshedTokens.refresh_token ?? token.refreshToken, // Mantener el refresh token anterior si no se envía uno nuevo
      roles: decodedToken?.realm_access?.roles,
      error: undefined, // Limpiar cualquier error anterior
    };
  } catch (error) {
    console.error("Error refreshing access token", error);
    return {
      ...token,
      error: "RefreshAccessTokenError", // Marcar el token con un error
    };
  }
}

export const authOptions: NextAuthOptions = {
  providers: [
    KeycloakProvider({
      clientId: process.env.KEYCLOAK_CLIENT_ID!,
      clientSecret: process.env.KEYCLOAK_CLIENT_SECRET!,
      issuer: process.env.KEYCLOAK_ISSUER!,
      wellKnown: process.env.KEYCLOAK_WELL_KNOWN_URL!,
      authorization: {
        params: {
          scope: "openid offline_access", // Solicitar solo los scopes necesarios
        },
      },
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    strategy: "jwt",
  },
  pages: {
    error: '/auth/error',
  },
  callbacks: {
    async jwt({ token, account }: { token: JWT, account: Account | null }): Promise<JWT> {
      const extendedToken = token as ExtendedJWT;

      // Inicio de sesión inicial
      if (account) {
        const decodedToken: DecodedToken | null = jwt.decode(account.access_token!) as DecodedToken | null;
        
        extendedToken.accessToken = account.access_token;
        extendedToken.refreshToken = account.refresh_token;
        extendedToken.accessTokenExpires = account.expires_at! * 1000;
        extendedToken.roles = decodedToken?.realm_access?.roles;
        return extendedToken;
      }

      // En peticiones posteriores, verificar si el token ha expirado
      if (Date.now() < extendedToken.accessTokenExpires!) {
        // Si no ha expirado, devolver el token existente
        return extendedToken;
      }

      // Si el token ha expirado, intentar refrescarlo
      console.log("Access token has expired, refreshing...");
      return refreshAccessToken(extendedToken);
    },
    async session({ session, token }: { session: Session, token: JWT }): Promise<Session> {
      const extendedSession = session as ExtendedSession;
      const extendedToken = token as ExtendedJWT;

      extendedSession.accessToken = extendedToken.accessToken;
      extendedSession.roles = extendedToken.roles;
      extendedSession.error = extendedToken.error;
      
      return extendedSession;
    }
  }
}

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST }