import { Test, TestingModule } from '@nestjs/testing';
import { ProductosController } from '../../productos.controller';
import { ProductosService } from '../../productos.service';
import { CreateProductoDto } from '../../dto/create-producto.dto';
import { UpdateProductoDto } from '../../dto/update-producto.dto';

describe('ProductosController', () => {
  let controller: ProductosController;
  let service: ProductosService;

  const mockProductosService = {
    findAll: jest.fn(),
    findOne: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    remove: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ProductosController],
      providers: [
        {
          provide: ProductosService,
          useValue: mockProductosService,
        },
      ],
    }).compile();

    controller = module.get<ProductosController>(ProductosController);
    service = module.get<ProductosService>(ProductosService);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('GET /productos', () => {
    it('debería retornar lista de productos con paginación', async () => {
      const mockResponse = {
        data: [{ id: 1, nombre: 'Producto Test' }],
        meta: { page: 1, limit: 10, total: 1, totalPages: 1 },
      };
      
      mockProductosService.findAll.mockResolvedValue(mockResponse);

      const result = await controller.findAll('1', '10', undefined, undefined);

      expect(result).toEqual(mockResponse);
      expect(service.findAll).toHaveBeenCalledWith(1, 10, undefined, undefined);
    });

    it('debería retornar lista de productos sin paginación', async () => {
      const mockResponse = {
        data: [{ id: 1, nombre: 'Producto Test' }],
      };
      
      mockProductosService.findAll.mockResolvedValue(mockResponse);

      const result = await controller.findAll(undefined, undefined, 'laptop', '1');

      expect(result).toEqual(mockResponse);
      expect(service.findAll).toHaveBeenCalledWith(undefined, undefined, 'laptop', 1);
    });
  });

  describe('GET /productos/:id', () => {
    it('debería retornar un producto específico', async () => {
      const mockProducto = { id: 1, nombre: 'Producto Test' };
      mockProductosService.findOne.mockResolvedValue(mockProducto);

      const result = await controller.findOne(1);

      expect(result).toEqual(mockProducto);
      expect(service.findOne).toHaveBeenCalledWith(1);
    });
  });

  describe('POST /productos', () => {
    it('debería crear un producto exitosamente', async () => {
      const createDto: CreateProductoDto = {
        nombre: 'Nuevo Producto',
        precio: 100,
        stockInicial: 10,
      };

      const mockResponse = { id: 1, mensaje: 'Producto creado exitosamente' };
      mockProductosService.create.mockResolvedValue(mockResponse);

      const result = await controller.create(createDto);

      expect(result).toEqual(mockResponse);
      expect(service.create).toHaveBeenCalledWith(createDto);
    });
  });

  describe('PATCH /productos/:id', () => {
    it('debería actualizar un producto', async () => {
      const updateDto: UpdateProductoDto = {
        nombre: 'Producto Actualizado',
        precio: 150,
      };

      const mockProducto = { id: 1, nombre: 'Producto Actualizado', precio: 150 };
      mockProductosService.update.mockResolvedValue(mockProducto);

      const result = await controller.update(1, updateDto);

      expect(result).toEqual(mockProducto);
      expect(service.update).toHaveBeenCalledWith(1, updateDto);
    });
  });

  describe('DELETE /productos/:id', () => {
    it('debería eliminar un producto', async () => {
      mockProductosService.remove.mockResolvedValue(undefined);

      await controller.remove(1);

      expect(service.remove).toHaveBeenCalledWith(1);
    });
  });
});