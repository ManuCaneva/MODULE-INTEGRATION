export class ProductoResponseDto {
  id: string;
  nombre: string;
  descripcion: string;
  precio: number;
  stockDisponible: number;
  pesoKg: number;
  imagenPrincipal: string;
  imagenes: string[];
}