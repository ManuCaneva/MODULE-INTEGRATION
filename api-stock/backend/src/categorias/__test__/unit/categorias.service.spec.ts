import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { CategoriasService } from '../../categorias.service';
import { Categoria } from '../../entities/categoria.entity';
import { NotFoundException } from '@nestjs/common';
import { CreateCategoriaDto } from '../../dto/create-categoria.dto';
import { UpdateCategoriaDto } from '../../dto/update-categoria.dto';

const mockCategoria: Categoria = {
  id: 1,
  nombre: 'Electrónica',
  activa: true,
};

const mockCategoriasArray: Categoria[] = [
  mockCategoria,
  { id: 2, nombre: 'Ropa', activa: true },
];

describe('CategoriasService', () => {
  let service: CategoriasService;
  let repository: Repository<Categoria>;

  const mockCategoriaRepository = {
    find: jest.fn().mockResolvedValue(mockCategoriasArray),
    findOne: jest.fn().mockResolvedValue(mockCategoria),
    create: jest.fn().mockImplementation((dto) => dto),
    save: jest.fn().mockImplementation((categoria) => Promise.resolve({ id: Date.now(), ...categoria })),
    merge: jest.fn().mockImplementation((categoria, dto) => ({...categoria, ...dto})),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        CategoriasService,
        {
          provide: getRepositoryToken(Categoria),
          useValue: mockCategoriaRepository,
        },
      ],
    }).compile();

    service = module.get<CategoriasService>(CategoriasService);
    repository = module.get<Repository<Categoria>>(getRepositoryToken(Categoria));
  });

  it('debería estar definido', () => {
    expect(service).toBeDefined();
  });

  describe('findAll()', () => {
    it('debería retornar un array de categorías activas ordenadas por nombre', async () => {
      const resultado = await service.findAll();
      expect(resultado).toEqual(mockCategoriasArray);
      expect(repository.find).toHaveBeenCalledWith({
        where: { activa: true },
        order: { nombre: 'ASC' },
      });
    });
  });

  describe('findOne()', () => {
    it('debería retornar una categoría si la encuentra', async () => {
      const id = 1;
      const resultado = await service.findOne(id);
      expect(resultado).toEqual(mockCategoria);
      expect(repository.findOne).toHaveBeenCalledWith({ where: { id, activa: true } });
    });

    it('debería lanzar NotFoundException si la categoría no existe', async () => {
      jest.spyOn(repository, 'findOne').mockResolvedValue(null);
      await expect(service.findOne(99)).rejects.toThrow(NotFoundException);
    });
  });

  describe('create()', () => {
    it('debería crear y retornar una nueva categoría', async () => {
      const dto: CreateCategoriaDto = { nombre: 'Juguetes' };
      jest.spyOn(repository, 'findOne').mockResolvedValue(null);
      const resultado = await service.create(dto);
      expect(resultado.nombre).toEqual(dto.nombre);
      expect(repository.findOne).toHaveBeenCalledWith({ where: { nombre: dto.nombre } });
      expect(repository.save).toHaveBeenCalled();
    });

    it('debería lanzar un Error si el nombre de la categoría ya existe', async () => {
      const dto: CreateCategoriaDto = { nombre: 'Electrónica' };
      jest.spyOn(repository, 'findOne').mockResolvedValue(mockCategoria);
      await expect(service.create(dto)).rejects.toThrow('Ya existe una categoría con ese nombre');
    });
  });

  describe('update()', () => {
    it('debería actualizar y retornar la categoría', async () => {
      const dto: UpdateCategoriaDto = { nombre: 'Tecnología' };
      jest.spyOn(repository, 'findOne').mockResolvedValueOnce(mockCategoria);
      jest.spyOn(repository, 'findOne').mockResolvedValueOnce(null);
      const resultado = await service.update(1, dto);
      expect(resultado.nombre).toEqual('Tecnología');
      expect(repository.save).toHaveBeenCalled();
    });

    it('debería lanzar un Error si se intenta actualizar a un nombre que ya existe', async () => {
      const dto: UpdateCategoriaDto = { nombre: 'Ropa' };
      const categoriaExistenteConEseNombre = { id: 2, nombre: 'Ropa', activa: true };
      jest.spyOn(repository, 'findOne').mockResolvedValueOnce(mockCategoria);
      jest.spyOn(repository, 'findOne').mockResolvedValueOnce(categoriaExistenteConEseNombre);
      await expect(service.update(1, dto)).rejects.toThrow('Ya existe una categoría con ese nombre');
    });
  });

  describe('remove()', () => {
    it('debería hacer un soft-delete cambiando el estado "activa" a false', async () => {
      const categoriaAActualizar = { ...mockCategoria };
      jest.spyOn(repository, 'findOne').mockResolvedValue(categoriaAActualizar);
      await service.remove(1);
      expect(repository.save).toHaveBeenCalledWith({ ...categoriaAActualizar, activa: false });
    });
  });
});