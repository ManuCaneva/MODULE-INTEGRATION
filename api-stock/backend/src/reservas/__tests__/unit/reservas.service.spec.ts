
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { ReservasService } from '../../reservas.service';
import { ProductosService } from '../../../productos/productos.service';
import { Reserva } from '../../entities/reserva.entity';
import { DetalleReserva } from '../../entities/detalle-reserva.entity';
import { ConflictException, NotFoundException } from '@nestjs/common';
import { ReservaInputDto } from '../../dto/create-reserva.dto';
import { UpdateReservaDto } from '../../dto/update-reserva.dto';
import { CancelacionReservaInputDto } from 'src/reservas/dto/delete-reserva.dto';

describe('ReservasService', () => {
  let service: ReservasService;
  let reservasRepository: Repository<Reserva>;
  let detallesRepository: Repository<DetalleReserva>;
  let productosService: ProductosService;
  let mockQueryBuilder: any;

  const mockReservasRepository = {
    create: jest.fn(),
    save: jest.fn(),
    findOne: jest.fn(),
    createQueryBuilder: jest.fn().mockReturnValue(mockQueryBuilder),
    preload: jest.fn(),
  };

  const mockDetallesRepository = {
    create: jest.fn(),
    save: jest.fn(),
  };

  const mockProductosService = {
    verificarStock: jest.fn(),
    reservarStock: jest.fn(),
    liberarStock: jest.fn(),
  };

  beforeEach(async () => {
    mockQueryBuilder = {
      leftJoinAndSelect: jest.fn().mockReturnThis(),
      where: jest.fn().mockReturnThis(),
      andWhere: jest.fn().mockReturnThis(),
      orderBy: jest.fn().mockReturnThis(),
      skip: jest.fn().mockReturnThis(),
      take: jest.fn().mockReturnThis(),
      getMany: jest.fn(),
      getManyAndCount: jest.fn(),
    };
    
    mockReservasRepository.createQueryBuilder.mockReturnValue(mockQueryBuilder);
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ReservasService,
        {
          provide: getRepositoryToken(Reserva),
          useValue: mockReservasRepository,
        },
        {
          provide: getRepositoryToken(DetalleReserva),
          useValue: mockDetallesRepository,
        },
        {
          provide: ProductosService,
          useValue: mockProductosService,
        },
      ],
    }).compile();

    service = module.get<ReservasService>(ReservasService);
    reservasRepository = module.get<Repository<Reserva>>(getRepositoryToken(Reserva));
    detallesRepository = module.get<Repository<DetalleReserva>>(getRepositoryToken(DetalleReserva));
    productosService = module.get<ProductosService>(ProductosService);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('reservar', () => {
    it('debería crear una reserva exitosamente', async () => {
      const reservaInput: ReservaInputDto = {
        idCompra: 'compra-123',
        usuarioId: 1, 
        productos: [{ idProducto: 1, cantidad: 2 }],
      };
      const mockReservaGuardada = { id: 1, estado: 'confirmado', expiresAt: new Date() };

      mockProductosService.verificarStock.mockResolvedValue(true);
      mockReservasRepository.create.mockReturnValue({ ...reservaInput, estado: 'confirmado' });
      mockReservasRepository.save.mockResolvedValue(mockReservaGuardada);
      mockDetallesRepository.create.mockReturnValue({});
      mockDetallesRepository.save.mockResolvedValue(undefined);
      mockProductosService.reservarStock.mockResolvedValue(undefined);

      const result = await service.reservar(reservaInput);

      expect(result.id).toBe(mockReservaGuardada.id);
      expect(result.estado).toBe('confirmado');
      expect(mockProductosService.verificarStock).toHaveBeenCalledWith(reservaInput.productos);
      expect(mockReservasRepository.save).toHaveBeenCalled();
      expect(mockDetallesRepository.save).toHaveBeenCalled();
      expect(mockProductosService.reservarStock).toHaveBeenCalledWith(reservaInput.productos);
    });

    it('debería lanzar ConflictException si no hay stock', async () => {
      const reservaInput: ReservaInputDto = {
        idCompra: 'compra-123',
        usuarioId: 1,
        productos: [{ idProducto: 1, cantidad: 10 }],
      };

      mockProductosService.verificarStock.mockResolvedValue(false);

      await expect(service.reservar(reservaInput)).rejects.toThrow(ConflictException);
      await expect(service.reservar(reservaInput)).rejects.toThrow('Stock insuficiente para realizar la reserva');
      expect(mockReservasRepository.save).not.toHaveBeenCalled();
    });
  });

  describe('liberar', () => {
    it('debería liberar el stock y cancelar la reserva', async () => {
      const liberacionInput: CancelacionReservaInputDto = {motivo: "Encontré otra oferta"};
      const mockReserva = {
        id: 1,
        estado: 'confirmado',
        detalles: [{ productoId: 1, cantidad: 2 }],
      };

      mockReservasRepository.findOne.mockResolvedValue(mockReserva);
      mockProductosService.liberarStock.mockResolvedValue(undefined);
      mockReservasRepository.save.mockResolvedValue({ ...mockReserva, estado: 'cancelado' });

      const result = await service.liberar(mockReserva.id, liberacionInput);

      expect(result.mensaje).toBe('Stock liberado exitosamente');
      expect(mockProductosService.liberarStock).toHaveBeenCalledWith([{ idProducto: 1, cantidad: 2 }]);
      expect(mockReservasRepository.save).toHaveBeenCalledWith({ ...mockReserva, estado: 'cancelado' });
    });

    it('debería lanzar NotFoundException si la reserva no existe', async () => {
      const liberacionInput: CancelacionReservaInputDto = {motivo: "Encontré otra oferta"};
      const idInexistente = 999;
      
      mockReservasRepository.findOne.mockResolvedValue(null);

      await expect(service.liberar(idInexistente, liberacionInput)).rejects.toThrow(NotFoundException);
      await expect(service.liberar(idInexistente, liberacionInput)).rejects.toThrow('Reserva no encontrada');
    });
  });

  describe('actualizar', () => {
    it('debería actualizar una reserva existente exitosamente', async () => {
      const idReserva = 1;
      const updateDto: UpdateReservaDto = { usuarioId: 1, estado: 'confirmado' }
      const mockReservaPreload = {
        id: idReserva,
        usuarioId: 1,
        estado: 'confirmado',
      };
      const mockReservaGuardada = { ...mockReservaPreload, ...updateDto };

      mockReservasRepository.preload.mockResolvedValue(mockReservaGuardada);
      mockReservasRepository.save.mockResolvedValue(mockReservaGuardada);

      const result = await service.actualizar(idReserva, updateDto);

      expect(reservasRepository.preload).toHaveBeenCalledWith({ id: idReserva, ...updateDto });
      expect(reservasRepository.save).toHaveBeenCalledWith(mockReservaGuardada);
      expect(result).toEqual(mockReservaGuardada);
    });

    it('debería lanzar NotFoundException si la reserva a actualizar no existe', async () => {
      const idReserva = 999;
      const updateDto: UpdateReservaDto = { usuarioId: 1, estado: 'confirmado' };

      mockReservasRepository.preload.mockResolvedValue(null);

      await expect(service.actualizar(idReserva, updateDto)).rejects.toThrow(
        new NotFoundException('Reserva no encontrada.'),
      );
      expect(reservasRepository.save).not.toHaveBeenCalled();
    });
  });

  describe('consultarReserva', () => {
    it('debería retornar los datos de una reserva existente', async () => {
      const mockReserva = { id: 1, usuarioId: 1, estado: 'confirmado', expiresAt: new Date() };
      mockReservasRepository.findOne.mockResolvedValue(mockReserva);

      const result = await service.consultarReserva(mockReserva.id, mockReserva.usuarioId);

      expect(result).toEqual({
        id: mockReserva.id,
        usuarioId: mockReserva.usuarioId,
        estado: mockReserva.estado,
        expiresAt: mockReserva.expiresAt,
      });
      expect(mockReservasRepository.findOne).toHaveBeenCalledWith({
        where: { 
          id: mockReserva.id, 
          usuarioId: mockReserva.usuarioId
        },
        relations: ['detalles'],
      });
    });

    it('debería lanzar NotFoundException si la reserva no se encuentra', async () => {
      mockReservasRepository.findOne.mockResolvedValue(null);
      const usuarioId = 1;

      await expect(service.consultarReserva(999, usuarioId)).rejects.toThrow(NotFoundException);
      await expect(service.consultarReserva(999, usuarioId)).rejects.toThrow('Reserva no encontrada');
    });
  });

  describe('consultarReservasDeUsuario', () => {
    it('debería retornar una lista paginada de reservas con filtro de estado', async () => {
      const usuarioId = 1;
      const options = { page: 1, limit: 10, estado: 'confirmado' };
      const mockReservas = [{ id: 1, usuarioId: 1, estado: 'confirmado' }];
      const totalReservas = 1;

      mockQueryBuilder.getManyAndCount.mockResolvedValue([mockReservas, totalReservas]);

      const result = await service.consultarReservasDeUsuario(usuarioId, options);

      expect(reservasRepository.createQueryBuilder).toHaveBeenCalledWith('reserva');
      expect(mockQueryBuilder.where).toHaveBeenCalledWith('reserva.usuarioId = :usuarioId', { usuarioId });
      expect(mockQueryBuilder.andWhere).toHaveBeenCalledWith('reserva.estado = :estado', { estado: options.estado });
      expect(mockQueryBuilder.skip).toHaveBeenCalledWith(0);
      expect(mockQueryBuilder.take).toHaveBeenCalledWith(10);
      expect(result.data).toEqual(mockReservas);
      expect(result.meta!.total).toBe(totalReservas);
      expect(result.meta!.page).toBe(options.page);
      });
    
    it('debería retornar todas las reservas de un usuario sin paginación', async () => {
      const usuarioId = 1;
      const options = {};
      const mockReservas = [
        { id: 1, usuarioId: 1, estado: 'confirmado' },
        { id: 2, usuarioId: 1, estado: 'cancelado' },
      ];
      mockQueryBuilder.getMany.mockResolvedValue(mockReservas);

      const result = await service.consultarReservasDeUsuario(usuarioId, options);

      expect(mockQueryBuilder.where).toHaveBeenCalledWith('reserva.usuarioId = :usuarioId', { usuarioId });
      expect(mockQueryBuilder.andWhere).not.toHaveBeenCalled();
      expect(mockQueryBuilder.skip).not.toHaveBeenCalled();
      expect(mockQueryBuilder.take).not.toHaveBeenCalled(); 
      expect(result.data).toEqual(mockReservas);
      expect(result.meta).toBeUndefined();
    });
  });
});
