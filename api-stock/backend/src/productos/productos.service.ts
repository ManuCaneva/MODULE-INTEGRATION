import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, In } from 'typeorm';
import { Producto } from './entities/producto.entity';
import { Categoria } from '../categorias/entities/categoria.entity';
import { CreateProductoDto } from './dto/create-producto.dto';
import { UpdateProductoDto } from './dto/update-producto.dto';
import { PaginatedResponse } from './interfaces/pagination.interface';
import { Dimensiones } from './entities/dimensiones.entity';
import { UbicacionAlmacen } from './entities/ubicacion-almacen.entity';
import { ImagenProducto } from './entities/imagen-producto.entity';

@Injectable()
export class ProductosService {
  constructor(
    @InjectRepository(Producto)
    private productosRepository: Repository<Producto>,
    @InjectRepository(Categoria)
    private categoriasRepository: Repository<Categoria>,
  ) {}

  async findAll(page?: number, limit?: number, search?: string, categoriaId?: number): Promise<PaginatedResponse<Producto>> {
    const query = this.productosRepository.createQueryBuilder('producto')
      .leftJoinAndSelect('producto.imagenes', 'imagenes')
      .leftJoinAndSelect('producto.categorias', 'categorias')
      .leftJoinAndSelect('producto.dimensiones', 'dimensiones')
      .leftJoinAndSelect('producto.ubicacion', 'ubicacion');

    if (search) {
      query.andWhere('producto.nombre LIKE :search', { search: `%${search}%` });
    }

    if (categoriaId) {
      query.andWhere('categorias.id = :categoriaId', { categoriaId });
    }

    query.orderBy('producto.id', 'DESC');

    const shouldPaginate = page !== undefined && limit !== undefined;
    
    if (shouldPaginate) {
      const validatedLimit = Math.max(1, Math.min(limit, 100));
      const validatedPage = Math.max(1, page);
      const skip = (validatedPage - 1) * validatedLimit;
      
      query.skip(skip).take(validatedLimit);
      const [data, total] = await query.getManyAndCount();

      return {
        data,
        meta: {
          page: validatedPage,
          limit: validatedLimit,
          total,
          totalPages: Math.ceil(total / validatedLimit),
        },
      };
    } else {
      const data = await query.getMany();
      return { data };
    }
  }

  async findOne(id: number): Promise<Producto> {
    const producto = await this.productosRepository.findOne({
      where: { id },
      relations: ['categorias', 'imagenes', 'dimensiones', 'ubicacion']
    });

    if (!producto) {
      throw new NotFoundException(`Producto con ID ${id} no encontrado`);
    }

    return producto;
  }

  async create(createProductoDto: CreateProductoDto): Promise<{ id: number; mensaje: string }> {
    const { categoriaIds, imagenes: imagenesUrls, stockInicial, ...productoData } = createProductoDto;

    let categorias: Categoria[] = [];
    if (categoriaIds && categoriaIds.length > 0) {
      categorias = await this.categoriasRepository.findBy({ id: In(categoriaIds) });
      if (categorias.length !== categoriaIds.length) {
        throw new BadRequestException('Una o más categorías no existen');
      }
    }

    const nuevoProducto = this.productosRepository.create({
      ...productoData,
      stockDisponible: stockInicial,
      categorias,
      // TypeORM creará las entidades relacionadas gracias a `cascade: true`
      dimensiones: productoData.dimensiones,
      ubicacion: productoData.ubicacion,
      imagenes: imagenesUrls?.map(url => ({ url, esPrincipal: false })) || [],
    });

    // Opcional: marcar la primera imagen como principal si no se especifica
    if (nuevoProducto.imagenes.length > 0) {
      nuevoProducto.imagenes[0].esPrincipal = true;
    }

    const productoGuardado = await this.productosRepository.save(nuevoProducto);

    return {
      id: productoGuardado.id,
      mensaje: 'Producto creado exitosamente'
    };
  }

  async update(id: number, updateProductoDto: UpdateProductoDto): Promise<Producto> {
    const { categoriaIds, imagenes: imagenesUrls, stockInicial, ...productoData } = updateProductoDto;
    
    const producto = await this.productosRepository.findOne({
        where: { id },
        relations: ['dimensiones', 'ubicacion', 'imagenes']
    });

    if (!producto) {
      throw new NotFoundException(`Producto con ID ${id} no encontrado`);
    }

    // Actualizar datos básicos y relaciones anidadas
    const updatedPayload = {
        ...producto,
        ...productoData,
        dimensiones: {
            ...producto.dimensiones,
            ...productoData.dimensiones,
        },
        ubicacion: {
            ...producto.ubicacion,
            ...productoData.ubicacion,
        }
    };

    if (stockInicial !== undefined) {
      updatedPayload.stockDisponible = stockInicial;
    }

    if (categoriaIds !== undefined) {
      if (categoriaIds.length > 0) {
        const categorias = await this.categoriasRepository.findBy({ id: In(categoriaIds) });
        if (categorias.length !== categoriaIds.length) {
          throw new BadRequestException('Una o más categorías no existen');
        }
        updatedPayload.categorias = categorias;
      } else {
        updatedPayload.categorias = [];
      }
    }

    if (imagenesUrls !== undefined) {
        // Reemplazar imágenes
        updatedPayload.imagenes = imagenesUrls.map(url => ({ url, esPrincipal: false })) as unknown as ImagenProducto[];
        if (updatedPayload.imagenes.length > 0) {
            updatedPayload.imagenes[0].esPrincipal = true;
        }
    }

    const updatedProduct = await this.productosRepository.save(updatedPayload);
    return updatedProduct;
  }

  async remove(id: number): Promise<void> {
    const result = await this.productosRepository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException(`Producto con ID ${id} no encontrado`);
    }
  }

  // Métodos de stock (sin cambios)
  async verificarStock(productos: Array<{ idProducto: number; cantidad: number }>): Promise<boolean> {
    for (const item of productos) {
      const producto = await this.productosRepository.findOneBy({ id: item.idProducto });
      if (!producto || producto.stockDisponible < item.cantidad) {
        return false;
      }
    }
    return true;
  }

  async reservarStock(productos: Array<{ idProducto: number; cantidad: number }>): Promise<void> {
    for (const item of productos) {
      await this.productosRepository.decrement({ id: item.idProducto }, 'stockDisponible', item.cantidad);
    }
  }

  async liberarStock(productos: Array<{ idProducto: number; cantidad: number }>): Promise<void> {
    for (const item of productos) {
      await this.productosRepository.increment({ id: item.idProducto }, 'stockDisponible', item.cantidad);
    }
  }
}