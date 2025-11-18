import { Injectable, ConflictException, NotFoundException, InternalServerErrorException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Reserva } from './entities/reserva.entity';
import { DetalleReserva } from './entities/detalle-reserva.entity';
import { ProductosService } from '../productos/productos.service';
import { ReservaInputDto } from './dto/create-reserva.dto';
import { UpdateReservaDto } from './dto/update-reserva.dto';
import { CancelacionReservaInputDto } from './dto/delete-reserva.dto';
import { PaginatedResponse } from 'src/productos/interfaces/pagination.interface';

@Injectable()
export class ReservasService {
  constructor(
    @InjectRepository(Reserva)
    private reservasRepository: Repository<Reserva>,
    @InjectRepository(DetalleReserva)
    private detallesRepository: Repository<DetalleReserva>,
    private productosService: ProductosService,
  ) {}

  async reservar(reservaInput: ReservaInputDto) {
    // Verificar stock disponible
    const stockDisponible = await this.productosService.verificarStock(reservaInput.productos);
    
    if (!stockDisponible) {
      throw new ConflictException('Stock insuficiente para realizar la reserva');
    }

    // Crear reserva
    const reserva = this.reservasRepository.create({
      idCompra: reservaInput.idCompra,
      usuarioId: reservaInput.usuarioId,
      estado: 'confirmado',
      expiresAt: new Date(Date.now() + 30 * 60 * 1000), // 30 minutos
    });

    const reservaGuardada = await this.reservasRepository.save(reserva);

    // Crear detalles de reserva
    const detalles = reservaInput.productos.map(item =>
      this.detallesRepository.create({
        reservaId: reservaGuardada.id,
        productoId: item.idProducto,
        cantidad: item.cantidad,
      })
    );

    await this.detallesRepository.save(detalles);

    // Reservar stock
    await this.productosService.reservarStock(reservaInput.productos);

    return reservaGuardada;
  }

  async liberar(idReserva: number, liberacionInput: CancelacionReservaInputDto) {
    const reserva = await this.reservasRepository.findOne({
      where: { id: idReserva },
      relations: ['detalles']
    });

    if (!reserva) {
      throw new NotFoundException('Reserva no encontrada');
    }

    // Liberar stock
    const productos = reserva.detalles.map(detalle => ({
      idProducto: detalle.productoId,
      cantidad: detalle.cantidad,
    }));

    await this.productosService.liberarStock(productos);

    // Actualizar estado de la reserva
    reserva.estado = 'cancelado';
    await this.reservasRepository.save(reserva);

    return {
      mensaje: 'Stock liberado exitosamente',
    };
  }
  
  async consultarReserva(idReserva: number, usuarioId: number) {
    const reserva = await this.reservasRepository.findOne({
      where: { 
        id: idReserva,
        usuarioId: usuarioId
      },
      relations: ['detalles']
    });

    if (!reserva) {
      throw new NotFoundException('Reserva no encontrada');
    }

    return reserva
  }

  async consultarReservasDeUsuario(usuarioId: number, options: {page?: number, limit?: number, estado?: string}): Promise<PaginatedResponse<Reserva>> {
    const {page, limit, estado} = options;

    const query = this.reservasRepository.createQueryBuilder('reserva')
      .leftJoinAndSelect('reserva.detalles', 'detalles');

    query.where('reserva.usuarioId = :usuarioId', { usuarioId });
    
    if (estado) {
      query.andWhere('reserva.estado = :estado', { estado });
    }

    query.orderBy('reserva.fechaCreacion', 'DESC');

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
      // Sin paginación - devolver todos los resultados
      const data = await query.getMany();
      
      return {
        data,
        // meta es opcional, así que no se incluye cuando no hay paginación
      };
    }
  }

  async actualizar(id: number, actualizacionInput: UpdateReservaDto) {
      const reserva = await this.reservasRepository.preload({
        id: id,
        ...actualizacionInput,
      });

      if (!reserva) {
        throw new NotFoundException(`Reserva no encontrada.`);
      }

      try {
        return await this.reservasRepository.save(reserva);
      } catch (error) {
        throw new InternalServerErrorException(`Error al actualizar la reserva: ${error.message}`);    
      }
  }
}