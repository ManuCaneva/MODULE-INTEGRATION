// frontend/src/app/page.tsx
"use client"; // Marcar como componente de cliente para usar hooks

import { Session } from "next-auth";
import { useSession } from "next-auth/react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import AuthButton from "@/components/ui/AuthButton"; // Importar el componente de autenticación

interface SessionWithRoles extends Session {
  roles?: string[];
}

export default function HomePage() {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center bg-gray-100 dark:bg-gray-900 p-8">
        <p>Cargando...</p>
      </main>
    );
  }

  if (status === "authenticated") {
    const roles = (session as SessionWithRoles)?.roles || [];
    const isVendedor = roles.includes("vendedor");

    return (
      <main className="flex min-h-screen flex-col items-center justify-center bg-gray-100 dark:bg-gray-900 p-8">
        <Card className="w-full max-w-lg">
          <CardHeader className="text-center">
            <CardTitle className="text-3xl font-bold">
              Bienvenido, {session.user?.name || session.user?.email}
            </CardTitle>
            <CardDescription className="text-lg pt-2">
              Has iniciado sesión correctamente.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col items-center space-y-4">
            <div>
              <h3 className="font-bold">Tus roles son:</h3>
              <ul>
                {roles.map((role: string) => (
                  <li key={role}>{role}</li>
                ))}
              </ul>
            </div>
            {isVendedor && (
              <div className="text-green-500 font-bold">
                ¡Eres un vendedor!
              </div>
            )}
            <AuthButton />
          </CardContent>
        </Card>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-100 dark:bg-gray-900 p-8">
      <Card className="w-full max-w-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold">
            Sistema de Gestión de Stock 📦
          </CardTitle>
          <CardDescription className="text-lg pt-2">
            Por favor, inicia sesión para continuar.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex justify-center">
          <AuthButton />
        </CardContent>
      </Card>
    </main>
  );
}
