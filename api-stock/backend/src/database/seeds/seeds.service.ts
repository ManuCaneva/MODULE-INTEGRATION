import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Categoria } from '../../categorias/entities/categoria.entity';
import { Producto } from '../../productos/entities/producto.entity';
import { Reserva } from '../../reservas/entities/reserva.entity';
import { Dimensiones } from '../../productos/entities/dimensiones.entity';
import { UbicacionAlmacen } from '../../productos/entities/ubicacion-almacen.entity';

@Injectable()
export class SeedsService {
  constructor(
    @InjectRepository(Categoria)
    private readonly categoriaRepository: Repository<Categoria>,
    @InjectRepository(Producto)
    private readonly productoRepository: Repository<Producto>,
    @InjectRepository(Reserva)
    private readonly reservaRepository: Repository<Reserva>,
    @InjectRepository(Dimensiones)
    private readonly dimensionesRepository: Repository<Dimensiones>,
    @InjectRepository(UbicacionAlmacen)
    private readonly ubicacionRepository: Repository<UbicacionAlmacen>,
  ) {}

  async loadData() {
    // --- INICIO DE MODIFICACIÓN ---
    // 1. Verificar si ya hay datos en la base de datos
    const count = await this.categoriaRepository.count();

    // 2. Si hay datos (count > 0), omitir el seeding
    if (count > 0) {
      console.log('La base de datos ya tiene datos. Omitiendo el seeding.');
      return;
    }

    // 3. Si no hay datos, proceder con el seeding
    console.log('Base de datos vacía. Iniciando el seeding...');
    await this.clearData();
    // --- FIN DE MODIFICACIÓN ---

    const categorias = await this.loadCategorias();
    const productos = await this.loadProductos(categorias);
    console.log('Seed data loaded successfully');
  }

  private async clearData() {
    await this.reservaRepository.query('TRUNCATE TABLE "reservas" CASCADE;');
    await this.productoRepository.query('TRUNCATE TABLE "productos" CASCADE;');
    await this.categoriaRepository.query('TRUNCATE TABLE "categorias" CASCADE;');
    await this.dimensionesRepository.query(
      'TRUNCATE TABLE "dimensiones" CASCADE;',
    );
    await this.ubicacionRepository.query(
      'TRUNCATE TABLE "ubicacion_almacen" CASCADE;',
    );
  }

  private async loadCategorias(): Promise<Categoria[]> {
    const categoriasData = [
      { nombre: 'Electrónicos' },
      { nombre: 'Ropa' },
      { nombre: 'Libros' },
    ];
    const categorias = this.categoriaRepository.create(categoriasData);
    await this.categoriaRepository.save(categorias);
    return categorias;
  }

  private async loadProductos(categorias: Categoria[]): Promise<Producto[]> {
    const productosData = [
      {
        nombre: 'Laptop Pro',
        descripcion: 'Una laptop potente para profesionales',
        precio: 1500.0,
        stockDisponible: 50,
        pesoKg: 1.8,
        dimensiones: {
          largoCm: 35.79,
          anchoCm: 24.59,
          altoCm: 1.62,
        },
        ubicacion: {
          street: 'Av. Vélez Sársfield 123',
          city: 'Resistencia',
          state: 'Chaco',
          postalCode: 'H3500ABC',
          country: 'AR',
        },
        imagenes: [
          { url: 'https://i.imgur.com/L6a2b3v.jpeg', esPrincipal: true },
          { url: 'https://i.imgur.com/L6a2b3v.jpeg', esPrincipal: false },
        ],
        categorias: [categorias.find((c) => c.nombre === 'Electrónicos')!],
      },
      {
        nombre: 'Camiseta de Algodón',
        descripcion: 'Camiseta cómoda para el día a día',
        precio: 25.0,
        stockDisponible: 200,
        pesoKg: 0.2,
        dimensiones: {
          largoCm: 70,
          anchoCm: 50,
          altoCm: 1,
        },
        ubicacion: {
          street: 'Av. 9 de Julio 1145',
          city: 'Resistencia',
          state: 'Chaco',
          postalCode: 'H3500ABC',
          country: 'AR',
        },
        imagenes: [
          { url: 'https://i.imgur.com/fQeImW2.jpeg', esPrincipal: true },
        ],
        categorias: [categorias.find((c) => c.nombre === 'Ropa')!],
      },
      {
        nombre: 'El Gran Gatsby',
        descripcion: 'Un clásico de la literatura',
        precio: 15.0,
        stockDisponible: 100,
        pesoKg: 0.3,
        dimensiones: {
          largoCm: 13.5,
          anchoCm: 20.3,
          altoCm: 1.3,
        },
        ubicacion: {
          street: 'Av. Sarmiento 550',
          city: 'Resistencia',
          state: 'Chaco',
          postalCode: 'H3500ABC',
          country: 'AR',
        },
        imagenes: [
          { url: 'https://i.imgur.com/d3b0b2e.jpeg', esPrincipal: true },
        ],
        categorias: [categorias.find((c) => c.nombre === 'Libros')!],
      },
    ];

    const productos = this.productoRepository.create(productosData);
    await this.productoRepository.save(productos);
    return productos;
  }
}