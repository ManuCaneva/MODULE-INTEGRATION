import type { PaginatedDashboardShipmentsResponse, ShippingDetail } from '$lib/types';
import { browser } from '$app/environment';

// --- 1. CONFIGURACIÓN DE URLS ---
// Tu lógica para la URL de la API (¡esto está perfecto!)
const API_BASE_URL = browser ? import.meta.env.VITE_PUBLIC_API_URL : import.meta.env.VITE_PRIVATE_API_URL;

// Configuración de Keycloak (como corre en el navegador, 'localhost' está bien)
const KEYCLOAK_URL = "http://localhost:8080/realms/ds-2025-realm/protocol/openid-connect/token";
const CLIENT_ID = "grupo-06";
const CLIENT_SECRET = "8dc00e75-ccea-4d1a-be3d-b586733e256c"; // El secreto que ya descubrimos

// --- 2. FUNCIÓN PARA OBTENER EL TOKEN (LA LLAVE) ---
async function getAuthToken(): Promise<string> {
    const body = new URLSearchParams();
    body.append("grant_type", "client_credentials");
    body.append("client_id", CLIENT_ID);
    body.append("client_secret", CLIENT_SECRET);

    try {
        const response = await fetch(KEYCLOAK_URL, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: body,
        });

        if (!response.ok) {
            throw new Error(`Error al obtener token de Keycloak: ${response.statusText}`);
        }

        const data = await response.json();
        return data.access_token;
    } catch (error) {
        console.error("Fallo grave en autenticación:", error);
        throw error; // Detenemos la ejecución si no hay token
    }
}

// --- 3. FUNCIÓN DE DASHBOARD (MODIFICADA) ---
export async function getDashboardShipments(page: number = 1, pageSize: number = 10): Promise<PaginatedDashboardShipmentsResponse> {
    const url = `${API_BASE_URL}/dashboard/shipments?page=${page}&pageSize=${pageSize}`;
    
    try {
        // A. Primero, conseguimos la llave
        const token = await getAuthToken();

        // B. Segundo, llamamos a la API con la llave
        const response = await fetch(url, {
            headers: {
                // Reemplazamos 'X-Internal-API-Key' por la autenticación correcta
                'Authorization': `Bearer ${token}`
            },
        });

        if (!response.ok) {
             if (response.status === 401 || response.status === 403) {
                console.error("¡Error de Autenticación! El token fue rechazado por la API.", response.statusText);
             }
            throw new Error(`Failed to fetch dashboard shipments: ${response.statusText}`);
        }
        return await response.json();

    } catch (error) {
        console.error("Error en getDashboardShipments:", error);
        throw error; // Dejamos que el componente Svelte maneje el error
    }
}

// Esta función ahora usa automáticamente la nueva autenticación
export async function getAllShipments(page: number = 1, page_size: number = 10): Promise<PaginatedDashboardShipmentsResponse> {
    return getDashboardShipments(page, page_size);
}

// Esta función es PÚBLICA (según la guía del profe), así que la dejamos como estaba.
export async function getShipmentById(id: string): Promise<ShippingDetail | undefined> {
    const response = await fetch(`${API_BASE_URL}/shipping/${id}`); // Sin token
    if (!response.ok) {
        if (response.status === 404) {
            return undefined; // Shipment not found
        }
        throw new Error(`Failed to fetch shipment ${id}: ${response.statusText}`);
    }
    const detailData: ShippingDetail = await response.json();
    return detailData;
}