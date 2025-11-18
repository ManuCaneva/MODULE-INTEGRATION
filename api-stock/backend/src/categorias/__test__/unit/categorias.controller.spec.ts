import { Test, TestingModule } from '@nestjs/testing';
import { CategoriasController } from '../../categorias.controller';
import { CategoriasService } from '../../categorias.service';
import { CreateCategoriaDto } from '../../dto/create-categoria.dto';
import { UpdateCategoriaDto } from '../../dto/update-categoria.dto';
import { Categoria } from './entities/categoria.entity';

const mockCategoria: Categoria = {
  id: 1,
  nombre: 'Electrónica',
};

describe('CategoriasController', () => {
  let controller: CategoriasController;
  let service: CategoriasService;

  const mockCategoriasService = {
    findAll: jest.fn().mockResolvedValue([mockCategoria]),
    findOne: jest.fn().mockImplementation((id: number) => 
      Promise.resolve({ ...mockCategoria, id })
    ),
    create: jest.fn().mockImplementation((dto: CreateCategoriaDto) => 
      Promise.resolve({ id: Date.now(), ...dto })
    ),
    update: jest.fn().mockImplementation((id: number, dto: UpdateCategoriaDto) =>
      Promise.resolve({ id, ...dto })
    ),
    remove: jest.fn().mockResolvedValue(undefined), 
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [CategoriasController],
      providers: [
        {
          provide: CategoriasService,
          useValue: mockCategoriasService,
    }
],
    }).compile();

    controller = module.get<CategoriasController>(CategoriasController);
    service = module.get<CategoriasService>(CategoriasService);
  });

  it('debería estar definido', () => {
    expect(controller).toBeDefined();
  });


  describe('findAll()', () => {
    it('debería retornar un array de categorías', async () => {
      const resultado = await controller.findAll();

      expect(resultado).toEqual([mockCategoria]);
      expect(service.findAll).toHaveBeenCalled(); 
    });
  });

  describe('findOne()', () => {
    it('debería retornar una única categoría por su ID', async () => {
      const id = 1;
      const resultado = await controller.findOne(id);

      expect(resultado.id).toEqual(id);
      expect(service.findOne).toHaveBeenCalledWith(id);
    });
  });

  describe('create()', () => {
    it('debería crear y retornar una nueva categoría', async () => {
      const dto: CreateCategoriaDto = { nombre: 'Ropa' };
      const resultado = await controller.create(dto);

      expect(resultado.nombre).toEqual(dto.nombre);
      expect(service.create).toHaveBeenCalledWith(dto);
    });
  });

  describe('update()', () => {
    it('debería actualizar y retornar la categoría modificada', async () => {
      const id = 1;
      const dto: UpdateCategoriaDto = { nombre: 'Tecnología' };
      const resultado = await controller.update(id, dto);

      expect(resultado.nombre).toEqual(dto.nombre);
      expect(service.update).toHaveBeenCalledWith(id, dto);
    });
  });

  describe('remove()', () => {
    it('debería eliminar una categoría y no retornar contenido', async () => {
      const id = 1;
      await controller.remove(id); // No se guarda en una variable porque no devuelve nada

      expect(service.remove).toHaveBeenCalledWith(id);
    });
  });
})