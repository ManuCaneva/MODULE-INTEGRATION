import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { ProductosService } from '../../productos.service';
import { Producto } from '../../entities/producto.entity';
import { Categoria } from '../../../categorias/entities/categoria.entity';
import { ImagenProducto } from '../../entities/imagen-producto.entity';
import { CreateProductoDto } from '../../dto/create-producto.dto';
import { UpdateProductoDto } from '../../dto/update-producto.dto';
import { BadRequestException, NotFoundException } from '@nestjs/common';
import { In } from 'typeorm';

describe('ProductosService', () => {
  let service: ProductosService;
  let productoRepository: Repository<Producto>;
  let categoriaRepository: Repository<Categoria>;
  let imagenRepository: Repository<ImagenProducto>;
  let mockQueryBuilder: any;

  const mockProductoRepository = {
    create: jest.fn(),
    save: jest.fn(),
    findOne: jest.fn(),
    findOneBy: jest.fn(),
    createQueryBuilder: jest.fn().mockReturnValue(mockQueryBuilder),
    decrement: jest.fn(),
    increment: jest.fn(),
  };
  
  const mockCategoriaRepository = {
    findBy: jest.fn(),
    count: jest.fn(),
  };

  const mockImagenRepository = {
    create: jest.fn(),
    save: jest.fn(),
    delete: jest.fn(),
  };

  beforeEach(async () => {
    mockQueryBuilder = {
      leftJoinAndSelect: jest.fn().mockReturnThis(),
      where: jest.fn().mockReturnThis(),
      andWhere: jest.fn().mockReturnThis(),
      orderBy: jest.fn().mockReturnThis(),
      skip: jest.fn().mockReturnThis(),
      take: jest.fn().mockReturnThis(),
      getManyAndCount: jest.fn(),
      getMany: jest.fn(),
    };

    mockProductoRepository.createQueryBuilder.mockReturnValue(mockQueryBuilder);
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ProductosService,
        {
          provide: getRepositoryToken(Producto),
          useValue: mockProductoRepository,
        },
        {
          provide: getRepositoryToken(Categoria),
          useValue: mockCategoriaRepository,
        },
        {
          provide: getRepositoryToken(ImagenProducto),
          useValue: mockImagenRepository,
        },
      ],
    }).compile();

    service = module.get<ProductosService>(ProductosService);
    productoRepository = module.get<Repository<Producto>>(getRepositoryToken(Producto));
    categoriaRepository = module.get<Repository<Categoria>>(getRepositoryToken(Categoria));
    imagenRepository = module.get<Repository<ImagenProducto>>(getRepositoryToken(ImagenProducto));
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('findAll', () => {
    it('debería retornar productos paginados cuando se envían page y limit', async () => {
      const mockProductos = [
        { id: 1, nombre: 'Producto 1', activo: true },
        { id: 2, nombre: 'Producto 2', activo: true }
      ];
      
      const queryBuilder = mockProductoRepository.createQueryBuilder();
      queryBuilder.getManyAndCount.mockResolvedValue([mockProductos, 2]);

      const result = await service.findAll(1, 10);

      expect(result.data).toEqual(mockProductos);
      expect(result.meta).toEqual({
        page: 1,
        limit: 10,
        total: 2,
        totalPages: 1
      });
      expect(queryBuilder.skip).toHaveBeenCalledWith(0);
      expect(queryBuilder.take).toHaveBeenCalledWith(10);
    });

    it('debería retornar todos los productos sin paginación cuando no se envían page y limit', async () => {
      const mockProductos = [
        { id: 1, nombre: 'Producto 1', activo: true },
        { id: 2, nombre: 'Producto 2', activo: true }
      ];
      
      const queryBuilder = mockProductoRepository.createQueryBuilder();
      queryBuilder.getMany.mockResolvedValue(mockProductos);

      const result = await service.findAll();

      expect(result.data).toEqual(mockProductos);
      expect(result.meta).toBeUndefined();
      expect(queryBuilder.getMany).toHaveBeenCalled();
    });

    it('debería aplicar filtro de búsqueda cuando se envía search', async () => {
      const queryBuilder = mockProductoRepository.createQueryBuilder();
      queryBuilder.getManyAndCount.mockResolvedValue([[], 0]);

      await service.findAll(1, 10, 'laptop');

      expect(queryBuilder.andWhere).toHaveBeenCalledWith('producto.nombre LIKE :search', { search: '%laptop%' });
    });

    it('debería aplicar filtro de categoría cuando se envía categoriaId', async () => {
      const queryBuilder = mockProductoRepository.createQueryBuilder();
      queryBuilder.getManyAndCount.mockResolvedValue([[], 0]);

      await service.findAll(1, 10, undefined, 1);

      expect(queryBuilder.andWhere).toHaveBeenCalledWith('categorias.id = :categoriaId', { categoriaId: 1 });
    });
  });

  describe('findOne', () => {
    it('debería retornar un producto existente', async () => {
      const mockProducto = { 
        id: 1, 
        nombre: 'Producto Test',
        dimensiones: {
          largoCm: 24.02,
          anchoCm: 12.5,
          altoCm: 2.22,
        },
        ubicacion: {
          street: "25 de Mayo",
          city: "Resistencia",
          state: "Chaco",
          postal_code: "H3500", 
          country: "AR"
        }, 
        activo: true,
        categorias: [],
        imagenes: []
      };
      
      mockProductoRepository.findOne.mockResolvedValue(mockProducto);

      const result = await service.findOne(1);

      expect(result).toEqual(mockProducto);
      expect(mockProductoRepository.findOne).toHaveBeenCalledWith({
        where: { id: 1 },
        relations: ['categorias', 'imagenes', 'dimensiones', 'ubicacion',]
      });
    });

    it('debería lanzar NotFoundException si el producto no existe', async () => {
      mockProductoRepository.findOne.mockResolvedValue(null);

      await expect(service.findOne(999)).rejects.toThrow(NotFoundException);
      await expect(service.findOne(999)).rejects.toThrow('Producto con ID 999 no encontrado');
    });
  });

  describe('create', () => {
    it('debería crear un producto exitosamente sin categorías ni imágenes', async () => {
      const createDto: CreateProductoDto = {
        nombre: 'Nuevo Producto',
        descripcion: 'Descripción',
        precio: 100,
        stockInicial: 10,
      };

      const mockProductoGuardado = { 
        id: 1, 
        ...createDto, 
        stockDisponible: 10 
      };

      mockProductoRepository.create.mockReturnValue({
        ...createDto,
        imagenes: [],
      });
      mockProductoRepository.save.mockResolvedValue(mockProductoGuardado);

      const result = await service.create(createDto);

      expect(result.id).toBe(1);
      expect(result.mensaje).toBe('Producto creado exitosamente');
      expect(mockProductoRepository.save).toHaveBeenCalled();
    });

    it('debería crear un producto con categorías e imágenes', async () => {
      const createDto: CreateProductoDto = {
        nombre: 'Producto con Categorías',
        precio: 200,
        stockInicial: 5,
        categoriaIds: [1, 2],
        imagenes: ['http://imagen1.jpg', 'http://imagen2.jpg']
      };

      const mockCategorias = [
        { id: 1, nombre: 'Electrónica' },
        { id: 2, nombre: 'Hogar' }
      ];

      const mockProductoGuardado = { 
        id: 1, 
        ...createDto, 
        stockDisponible: 5,
        categorias: mockCategorias
      };

      mockCategoriaRepository.findBy.mockResolvedValue(mockCategorias);
      mockProductoRepository.create.mockImplementation(dto => ({
        ...dto,
        imagenes: dto.imagenes ? dto.imagenes.map(url => ({ url, esPrincipal: false })) : [],
      }));
      mockProductoRepository.save.mockResolvedValue(mockProductoGuardado);

      const result = await service.create(createDto);

      expect(result.id).toBe(1);
    });

    it('debería lanzar BadRequestException si categorías no existen', async () => {
      const createDto: CreateProductoDto = {
        nombre: 'Producto Test',
        precio: 100,
        stockInicial: 10,
        categoriaIds: [1, 2],
      };

      mockCategoriaRepository.findBy.mockResolvedValue([]); // No categories found

      await expect(service.create(createDto)).rejects.toThrow(BadRequestException);
      await expect(service.create(createDto)).rejects.toThrow('Una o más categorías no existen');
    });
  });

  describe('verificarStock', () => {
    const productos = [{ idProducto: 1, cantidad: 5 }];
    const mockProducto = { id: 1, stockDisponible: 10 };

    it('debería retornar true si hay stock suficiente', async () => {
      mockProductoRepository.findOneBy.mockResolvedValue(mockProducto);

      const result = await service.verificarStock(productos);

      expect(result).toBe(true);
    });

    it('debería retornar false si no hay stock suficiente', async () => {
      const productos = [{ idProducto: 1, cantidad: 15 }];
      const mockProducto = { id: 1, stockDisponible: 10 };
      mockProductoRepository.findOneBy.mockResolvedValue(mockProducto);

      const result = await service.verificarStock(productos);

      expect(result).toBe(false);
    });

    it('debería retornar false si el producto no existe', async () => {
      const productos = [{ idProducto: 999, cantidad: 1 }];

      mockProductoRepository.findOneBy.mockResolvedValue(null);

      const result = await service.verificarStock(productos);

      expect(result).toBe(false);
    });
  });

  describe('reservarStock y liberarStock', () => {
    it('debería reservar stock correctamente', async () => {
      const productos = [{ idProducto: 1, cantidad: 3 }];

      await service.reservarStock(productos);

      expect(mockProductoRepository.decrement).toHaveBeenCalledWith(
        { id: 1 },
        'stockDisponible',
        3
      );
    });

    it('debería liberar stock correctamente', async () => {
      const productos = [{ idProducto: 1, cantidad: 3 }];

      await service.liberarStock(productos);

      expect(mockProductoRepository.increment).toHaveBeenCalledWith(
        { id: 1 },
        'stockDisponible',
        3
      );
    });
  });
});