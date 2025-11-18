
import { Test, TestingModule } from '@nestjs/testing';
import { ReservaController } from '../../reservas.controller';
import { ReservasService } from '../../reservas.service';
import { ReservaInputDto } from '../../dto/create-reserva.dto';
import { UpdateReservaDto } from '../../dto/update-reserva.dto';
import { CancelacionReservaInputDto } from 'src/reservas/dto/delete-reserva.dto';

describe('ReservaController', () => {
  let controller: ReservaController;
  let service: ReservasService;

  const mockReservasService = {
    reservar: jest.fn(),
    liberar: jest.fn(),
    consultarReserva: jest.fn(),
    actualizar: jest.fn(),
    consultarReservasDeUsuario: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ReservaController],
      providers: [
        {
          provide: ReservasService,
          useValue: mockReservasService,
        },
      ],
    }).compile();

    controller = module.get<ReservaController>(ReservaController);
    service = module.get<ReservasService>(ReservasService);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });
    
  describe('GET /', () => {
    it('debería retornar lista de reservas de un usuario con paginación', async () => {
      const usuarioId = 1;
      const estado = 'pendiente';

      const mockResponse = { data: [], meta: { total: 0 } };
      mockReservasService.consultarReservasDeUsuario.mockResolvedValue(mockResponse);

      const result = await controller.consultarReservasDeUsuario(usuarioId, '1', '5', estado);

      expect(result).toEqual(mockResponse);
      expect(service.consultarReservasDeUsuario).toHaveBeenCalledTimes(1);
      expect(service.consultarReservasDeUsuario).toHaveBeenCalledWith(usuarioId, {
        page: 1, 
        limit: 5, 
        estado: estado});
    });

    it('debería retornar todas las reservas de un usuario cuando no se pagina', async () => {
      const usuarioId = 1;

      const mockResponse = { data: [] };
      mockReservasService.consultarReservasDeUsuario.mockResolvedValue(mockResponse);

      const result = await controller.consultarReservasDeUsuario(usuarioId,
        undefined,
        undefined,
        undefined
      );

      expect(result).toEqual(mockResponse);
      expect(service.consultarReservasDeUsuario).toHaveBeenCalledTimes(1);
      expect(service.consultarReservasDeUsuario).toHaveBeenCalledWith(usuarioId, {
        page: undefined,
        limit: undefined,
        estado: undefined,
      });
    });
  });

  describe('POST /', () => {
    it('debería llamar al servicio de reservar con los datos correctos', async () => {
      const reservaInput: ReservaInputDto = {
        idCompra: 'compra-123',
        usuarioId: 1,
        productos: [{ idProducto: 1, cantidad: 2 }],
      };
      const mockResponse = { idReserva: 1, usuarioId: 1, estado: 'confirmado', expiresAt: new Date() };

      mockReservasService.reservar.mockResolvedValue(mockResponse);

      const result = await controller.reservar(reservaInput);

      expect(result).toEqual(mockResponse);
      expect(service.reservar).toHaveBeenCalledWith(reservaInput);
    });
  });

  describe('DELETE /:idReserva', () => {
    it('debería llamar al servicio de liberar con los datos correctos', async () => {
      const idReserva = 1;
      const liberacionInput: CancelacionReservaInputDto = { motivo: 'Me arrepentí' };
      const mockResponse = { mensaje: 'Stock liberado exitosamente' };

      mockReservasService.liberar.mockResolvedValue(mockResponse);

      const result = await controller.liberar(idReserva, liberacionInput);

      expect(result).toEqual(mockResponse);
      expect(service.liberar).toHaveBeenCalledWith(idReserva, liberacionInput);
    });
  });

  describe('GET /:idReserva', () => {
    it('debería llamar al servicio de consultarReserva con el ID correcto', async () => {
      const mockResponse = { idReserva: 1, estado: 'confirmado', expiresAt: new Date() };
      const usuarioId = 1; 

      mockReservasService.consultarReserva.mockResolvedValue(mockResponse);

      const result = await controller.consultarReserva(1, usuarioId);

      expect(result).toEqual(mockResponse);
      expect(service.consultarReserva).toHaveBeenCalledWith(1, usuarioId);
    });
  });

  describe('PATCH /:idReserva', () => {
    it('debería llamar al servicio de actualizar con el ID correcto', async () => {
      const idReserva = 1;
      const actualizacionInput: UpdateReservaDto = {
        usuarioId: 1,
        estado: 'confirmado'
      }
      const mockResponse = { id: 1, ...actualizacionInput };

      mockReservasService.actualizar.mockResolvedValue(mockResponse);

      const result = await controller.update(idReserva, actualizacionInput);

      expect(result).toEqual(mockResponse);
      expect(service.actualizar).toHaveBeenCalledWith(idReserva, actualizacionInput);
    });
  });
});
