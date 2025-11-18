export interface Dimensiones {
  largoCm: number;
  anchoCm: number;
  altoCm: number;
}

export interface UbicacionAlmacen {
  street: string;
  city: string;
  state: string;
  postalCode: string;
  country: string;
}

export interface ImagenProducto {
  url: string;
  esPrincipal: boolean;
}

export interface Category {
  id: number;
  nombre: string;
  descripcion?: string | null;
}

export interface CategoriaInput {
  nombre: string;
  descripcion?: string | null;
}

export interface Product {
  id: number;
  nombre: string;
  descripcion?: string;
  precio: number;
  stockDisponible: number;
  pesoKg?: number;
  dimensiones?: Dimensiones;
  ubicacion?: UbicacionAlmacen;
  imagenes?: ImagenProducto[];
  categorias?: Category[];
}

export interface ProductoInput {
  nombre: string;
  descripcion?: string;
  precio: number;
  stockInicial: number;
  pesoKg?: number;
  dimensiones?: Dimensiones;
  ubicacion: UbicacionAlmacen; // <-- Hacemos que coincida con el DTO del backend
  imagenes?: ImagenProducto[];
  categoriaIds?: number[];
}

export interface ProductoUpdate {
  nombre?: string;
  descripcion?: string;
  precio?: number;
  stockInicial?: number;
  pesoKg?: number;
  dimensiones?: Dimensiones;
  ubicacion?: UbicacionAlmacen;
  imagenes?: ImagenProducto[];
  categoriaIds?: number[];
}

export interface ProductoCreado {
  id: number;
  mensaje: string;
}

export interface PaginatedProducts {
  items: Product[];
  total: number;
  page: number;
  limit: number;
}

export interface PaginatedReservas {
  items: ReservaCompleta[];
  total: number;
  page: number;
  limit: number;
}

export interface ReservaInput {
  idCompra: string;
  usuarioId: number;
  productos: {
    idProducto: number;
    cantidad: number;
  }[];
}

export interface ReservaOutput {
  idReserva: number;
  idCompra: string;
  usuarioId: number;
  estado: 'confirmado' | 'pendiente' | 'cancelado';
  expiresAt: string;
  fechaCreacion: string;
}

export interface ReservaCompleta {
    idReserva: number;
    idCompra: string;
    usuarioId: number;
    estado: 'confirmado' | 'pendiente' | 'cancelado';
    expiresAt: string;
    fechaCreacion: string;
    fechaActualizacion: string;
    productos: {
        idProducto: number;
        nombre: string;
        cantidad: number;
        precioUnitario: number;
    }[];
}

export interface ActualizarReservaInput {
    usuarioId: number;
    estado: 'confirmado' | 'pendiente' | 'cancelado';
}

export interface CancelacionReservaInput {
    motivo: string;
}


export const getCategory = (id: number, cats: Category[]) => {
  return cats.find((cat) => cat.id === id);
};
