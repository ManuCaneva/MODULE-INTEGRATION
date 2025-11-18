export type ID = number;

export interface Category {
  id: ID;
  nombre: string;
  activo: boolean;
  createdAt?: string;
  updatedAt?: string;
}

export interface Product {
  id: ID;
  nombre: string;
  descripcion?: string;
  precio: number;
  stock: number;
  categoriaId: ID;
  categoria?: Category;
  activo: boolean;
  createdAt?: string;
  updatedAt?: string;
}

export interface Paginated<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}

export interface ReservationItem {
  productoId: ID;
  cantidad: number;
}

export interface Reservation {
  id: ID;
  items: Array<{ producto: Product; cantidad: number }>;
  estado: "RESERVADA" | "LIBERADA" | "CONSUMIDA";
  createdAt?: string;
}
