// frontend/src/components/AuthButton.tsx
"use client"; // Marcar como componente de cliente

import { useSession, signIn, signOut } from "next-auth/react";

export default function AuthButton() {
  // Obtener la sesión y el estado de autenticación
  const { data: session, status } = useSession();

  // Mostrar un mensaje mientras se carga la sesión
  if (status === "loading") {
    return <p style={{ color: 'gray' }}>Cargando sesión...</p>;
  }

  // Si el usuario está autenticado
  if (session) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span>¡Hola, {session.user?.name || session.user?.email || 'Usuario'}!</span>
        <button 
          onClick={() => signOut()}
          style={{ padding: '5px 10px', cursor: 'pointer' }}
        >
          Cerrar Sesión
        </button>
      </div>
    );
  }

  // Si el usuario no está autenticado
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
      <span>No has iniciado sesión</span>
      <button 
        onClick={() => signIn("keycloak", { callbackUrl: "/products" })} // Llama al proveedor 'keycloak' que configuraste
        style={{ padding: '5px 10px', cursor: 'pointer' }}
      >
        Iniciar Sesión con Keycloak
      </button>
    </div>
  );
}