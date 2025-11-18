import { Product, Category } from './definitions';

export const mockCategories: Category[] = [
  { id: 1, nombre: 'Electrónica', descripcion: 'Dispositivos electrónicos y accesorios.' },
  { id: 2, nombre: 'Libros', descripcion: 'Libros de todo tipo.' },
  { id: 3, nombre: 'Ropa', descripcion: 'Ropa para todas las edades.' },
  { id: 4, nombre: 'Hogar', descripcion: 'Artículos para el hogar y decoración.' },
  { id: 5, nombre: 'Deportes', descripcion: 'Artículos deportivos.' },
  { id: 6, nombre: 'Juguetes', descripcion: 'Juguetes para niños.' },
  { id: 7, nombre: 'Jardín', descripcion: 'Artículos de jardinería.' },
  { id: 8, nombre: 'Automotriz', descripcion: 'Repuestos y accesorios para vehículos.' },
  { id: 9, nombre: 'Salud', descripcion: 'Productos de salud y bienestar.' },
  { id: 10, nombre: 'Alimentos', descripcion: 'Alimentos y bebidas.' },
  { id: 11, nombre: 'Música', descripcion: 'Instrumentos y álbumes musicales.' },
  { id: 12, nombre: 'Películas', descripcion: 'Películas en DVD y Blu-ray.' },
  { id: 13, nombre: 'Herramientas', descripcion: 'Herramientas para el hogar y el trabajo.' },
  { id: 14, nombre: 'Mascotas', descripcion: 'Comida y accesorios para mascotas.' },
  { id: 15, nombre: 'Belleza', descripcion: 'Productos de belleza y cuidado personal.' }
];

export const mockProducts: Product[] = [
  {
    id: 1,
    nombre: 'Laptop Pro X',
    descripcion: 'Una laptop potente para profesionales.',
    precio: 1499.99,
    stockDisponible: 50,
    pesoKg: 1.8,
    dimensiones: { largoCm: 35, anchoCm: 25, altoCm: 2 },
    ubicacion: { almacenId: 1, pasillo: 'A', estanteria: '3', nivel: 2 },
    imagenes: [{ url: 'https://example.com/images/laptop.jpg', esPrincipal: true }],
    categorias: [mockCategories[0], mockCategories[4]]
  },
  {
    id: 2,
    nombre: 'El Señor de los Anillos',
    descripcion: 'La trilogía completa en una edición de lujo.',
    precio: 79.99,
    stockDisponible: 100,
    pesoKg: 1.2,
    categorias: [mockCategories[1]]
  },
  {
    id: 3,
    nombre: 'Camiseta de Algodón',
    descripcion: 'Camiseta básica de algodón en varios colores.',
    precio: 19.99,
    stockDisponible: 200,
    categorias: [mockCategories[2]]
  },
  {
    id: 4,
    nombre: 'Sofá Moderno',
    descripcion: 'Un sofá de 3 plazas con diseño moderno.',
    precio: 899.99,
    stockDisponible: 20,
    dimensiones: { largoCm: 200, anchoCm: 90, altoCm: 80 },
    categorias: [mockCategories[3]]
  },
  {
    id: 5,
    nombre: 'Balón de Baloncesto',
    descripcion: 'Balón oficial de la NBA.',
    precio: 29.99,
    stockDisponible: 0,
    categorias: [mockCategories[4]]
  },
  {
    id: 6,
    nombre: 'Set de Lego Classic',
    descripcion: 'Caja grande de ladrillos creativos.',
    precio: 49.99,
    stockDisponible: 80,
    categorias: [mockCategories[5]]
  },
  {
    id: 7,
    nombre: 'Cortacésped Eléctrico',
    descripcion: 'Cortacésped silencioso y eficiente.',
    precio: 299.99,
    stockDisponible: 30,
    pesoKg: 15,
    categorias: [mockCategories[6]]
  },
  {
    id: 8,
    nombre: 'Aceite de Motor Sintético',
    descripcion: 'Garrafa de 5 litros de aceite 5W-30.',
    precio: 45.50,
    stockDisponible: 120,
    categorias: [mockCategories[7]]
  },
  {
    id: 9,
    nombre: 'Multivitamínico',
    descripcion: 'Frasco con 90 cápsulas.',
    precio: 24.99,
    stockDisponible: 300,
    categorias: [mockCategories[8]]
  },
  {
    id: 10,
    nombre: 'Manzanas Frescas',
    descripcion: 'Bolsa de 1kg de manzanas rojas.',
    precio: 3.99,
    stockDisponible: 500,
    categorias: [mockCategories[9]]
  }
];

export const getProductById = (id: number) => {
  return mockProducts.find(p => p.id === id);
}