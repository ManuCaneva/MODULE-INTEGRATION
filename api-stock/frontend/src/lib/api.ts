import { getSession } from 'next-auth/react';
import { PaginatedProducts, Category, Product, ReservaInput, ReservaOutput, ReservaCompleta, CancelacionReservaInput, ActualizarReservaInput, ProductoInput, ProductoUpdate, ProductoCreado, CategoriaInput, PaginatedReservas } from './definitions';

const API_BASE_URL = typeof window === 'undefined' 
    ? process.env.NEXT_PUBLIC_API_URL || 'http://backend:3000' 
    : '/api';

interface Session {
    accessToken?: string;
}

async function fetcher<T>(url: string, options: RequestInit = {}, token?: string | null): Promise<T> {
    try {
        let sessionToken = token; // Usar el token pasado si existe

        // Si no se pasó un token, intentar obtenerlo de la sesión (lado cliente)
        if (sessionToken === undefined) { 
            const session: Session | null = await getSession();
            sessionToken = session?.accessToken;
            console.log('Fetcher - Session Client-Side:', session); // Log lado cliente
        } else {
             console.log('Fetcher - Token Passed Server-Side:', sessionToken?.substring(0, 30) + '...'); // Log lado servidor
        }


        const newOptions = { ...options };
        newOptions.headers = { ...newOptions.headers } as Record<string, string>;

        if (sessionToken) { // Usar la variable sessionToken
            newOptions.headers['Authorization'] = `Bearer ${sessionToken}`;
            console.log('Fetcher - Token Added:', newOptions.headers['Authorization']?.substring(0, 30) + '...');
        } else {
             console.log('Fetcher - No token available or passed.');
        }

        // No establecer Content-Type si el body es FormData
        if (newOptions.body && !(newOptions.body instanceof FormData)) {
            if (!newOptions.headers['Content-Type']) {
                newOptions.headers['Content-Type'] = 'application/json';
            }
        }

        const response = await fetch(url, newOptions);

        if (!response.ok) {
            const errorBody = await response.text();
            console.error(`HTTP error! status: ${response.status}`, errorBody);
            throw new Error(`Error en la petición: ${response.statusText}`);
        }

        if (response.status === 204) {
            return undefined as T;
        }

        return response.json();

    } catch (error) {
        console.error("Error en fetcher:", error);
        throw error;
    }
}

// ===== Productos =====
interface BackendPaginatedProducts {
    items?: Product[];
    data?: Product[];
    total?: number;
    meta?: {
        totalItems?: number;
        currentPage?: number;
        itemsPerPage?: number;
    };
    page?: number;
    limit?: number;
}

export async function listarProductos(
    page: number = 1,
    limit: number = 10,
    q: string = '',
    categoriaId?: number
): Promise<PaginatedProducts> {
    const params = new URLSearchParams({
        page: page.toString(),
        limit: limit.toString(),
    });

    if (q) {
        params.append('q', q);
    }

    if (categoriaId) {
        params.append('categoriaId', categoriaId.toString());
    }
    
    const data = await fetcher<BackendPaginatedProducts>(`${API_BASE_URL}/productos?${params.toString()}`, { cache: 'no-store' });

    return {
        items: data.items ?? data.data ?? [],
        total: data.total ?? data.meta?.totalItems ?? 0,
        page: data.page ?? data.meta?.currentPage ?? page,
        limit: data.limit ?? data.meta?.itemsPerPage ?? limit,
    };
}


export async function obtenerProductoPorId(id: number, token?: string | null): Promise<Product> {
    // Pasar el token a fetcher
    return fetcher<Product>(`${API_BASE_URL}/productos/${id}`, { cache: 'no-store' }, token);
}

export async function crearProducto(
    productData: ProductoInput,
    token?: string
): Promise<ProductoCreado> {
    // Paso 1: Crear el producto con los datos de texto/numéricos.
    return fetcher<ProductoCreado>(`${API_BASE_URL}/productos`, {
        method: 'POST',
        body: JSON.stringify(productData),
        headers: {
            'Content-Type': 'application/json',
        }
    }, token);
}

export async function uploadImage(productId: number, image: File, token?: string): Promise<void> {
    const formData = new FormData();
    // El nombre 'file' debe coincidir con el que espera el backend (usualmente definido en el FileInterceptor)
    formData.append('file', image);
  
    // Asumimos que el endpoint del backend es /productos/{id}/upload
    return fetcher<void>(`${API_BASE_URL}/productos/${productId}/upload`, {
      method: 'POST',
      body: formData,
    }, token);
}

export async function actualizarProducto(id: number, body: ProductoUpdate): Promise<Product> {
    return fetcher<Product>(`${API_BASE_URL}/productos/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(body),
    });
}

export async function eliminarProducto(id: number) {
    return fetcher<void>(`${API_BASE_URL}/productos/${id}`, { method: 'DELETE' });
}

// ===== Categorías =====
export async function getCategories(token?: string): Promise<Category[]> {
    return fetcher<Category[]>(`${API_BASE_URL}/categorias`, { cache: 'no-store' }, token);
}

export async function obtenerCategoriaPorId(id: number): Promise<Category> {
    return fetcher<Category>(`${API_BASE_URL}/categorias/${id}`, { cache: 'no-store' });
}

export async function crearCategoria(body: CategoriaInput): Promise<Category> {
    return fetcher<Category>(`${API_BASE_URL}/categorias`, {
        method: 'POST',
        body: JSON.stringify(body),
    });
}

export async function actualizarCategoria(id: number, body: CategoriaInput): Promise<Category> {
    return fetcher<Category>(`${API_BASE_URL}/categorias/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(body),
    });
}

export async function eliminarCategoria(id: number, token?: string) {
    return fetcher<void>(`${API_BASE_URL}/categorias/${id}`, { method: 'DELETE' }, token);
}

// ===== Reservas =====
interface BackendPaginatedReservas {
    items?: ReservaCompleta[];
    data?: ReservaCompleta[];
    total?: number;
    meta?: {
        totalItems?: number;
        currentPage?: number;
        itemsPerPage?: number;
    };
    page?: number;
    limit?: number;
}

export async function listarReservas(
    usuarioId: number,
    page: number = 1,
    limit: number = 10,
    estado?: 'confirmado' | 'pendiente' | 'cancelado'
): Promise<PaginatedReservas> {
    const params = new URLSearchParams({
        usuarioId: usuarioId.toString(),
        page: page.toString(),
        limit: limit.toString(),
    });
    if (estado) {
        params.append('estado', estado);
    }
    
    const data = await fetcher<BackendPaginatedReservas>(`${API_BASE_URL}/reservas?${params.toString()}`, { cache: 'no-store' });

    return {
        items: data.items ?? data.data ?? [],
        total: data.total ?? data.meta?.totalItems ?? 0,
        page: data.page ?? data.meta?.currentPage ?? page,
        limit: data.limit ?? data.meta?.itemsPerPage ?? limit,
    };
}

export async function obtenerReservaPorId(idReserva: number): Promise<ReservaCompleta> {
    const params = new URLSearchParams({
        // usuarioId: usuarioId.toString(),
    });
    return fetcher<ReservaCompleta>(`${API_BASE_URL}/reservas/${idReserva}?${params.toString()}`, { cache: 'no-store' });
}

export async function crearReserva(input: ReservaInput): Promise<ReservaOutput> {
    return fetcher<ReservaOutput>(`${API_BASE_URL}/reservas`, {
        method: 'POST',
        body: JSON.stringify(input),
    });
}

export async function actualizarReserva(idReserva: number, input: ActualizarReservaInput): Promise<ReservaCompleta> {
    return fetcher<ReservaCompleta>(`${API_BASE_URL}/reservas/${idReserva}`, {
        method: 'PATCH',
        body: JSON.stringify(input),
    });
}

export async function cancelarReserva(idReserva: number, input: CancelacionReservaInput): Promise<void> {
    return fetcher<void>(`${API_BASE_URL}/reservas/${idReserva}`, {
        method: 'DELETE',
        body: JSON.stringify(input),
    });
}