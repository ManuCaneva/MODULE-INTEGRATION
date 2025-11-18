'use client';

import { useSession, signOut } from "next-auth/react";
import { useEffect } from "react";

// Definir el tipo de la sesión extendida
interface ExtendedSession {
  error?: string;
}

const SessionErrorHandler = () => {
  const { data: session } = useSession();

  useEffect(() => {
    const extendedSession = session as ExtendedSession;
    if (extendedSession?.error === "RefreshAccessTokenError") {
      // Forzar cierre de sesión si hay un error al refrescar el token
      signOut({ callbackUrl: '/' });
    }
  }, [session]);

  return null; // Este componente no renderiza nada
};

export default SessionErrorHandler;
