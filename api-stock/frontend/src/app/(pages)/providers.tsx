// frontend/src/app/providers.tsx
"use client"; // Marcar como componente de cliente

import { SessionProvider } from "next-auth/react";

export const NextAuthProvider = ({ children }: { children: React.ReactNode }) => {
  return <SessionProvider>{children}</SessionProvider>;
};