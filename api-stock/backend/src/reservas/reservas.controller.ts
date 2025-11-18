import { Controller, Post, Get, Body, Param, ParseIntPipe, Delete, Patch, Query, DefaultValuePipe, UseGuards } from '@nestjs/common';
import { ReservasService } from './reservas.service';
import { ReservaInputDto } from './dto/create-reserva.dto';
import { UpdateReservaDto } from './dto/update-reserva.dto';
import { CancelacionReservaInputDto } from './dto/delete-reserva.dto';
import { PaginatedResponse } from 'src/productos/interfaces/pagination.interface';
import { Reserva } from './entities/reserva.entity';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { ScopesGuard } from '../auth/scopes.guard';
import { Scopes } from '../auth/scopes.decorator';

@Controller('reservas')
@UseGuards(JwtAuthGuard, ScopesGuard)
export class ReservaController {
  constructor(private readonly reservaService: ReservasService) {}

  @Post('/')
  @Scopes('reservas:write')
  async reservar(@Body() reservaInput: ReservaInputDto): Promise<Reserva> {
    return this.reservaService.reservar(reservaInput);
  }

  @Delete('/:idReserva')
  @Scopes('reservas:write')
  async liberar(@Param('idReserva', ParseIntPipe) idReserva: number,
                @Body() cancelacionInput: CancelacionReservaInputDto): Promise<{ mensaje: string }> {
    return this.reservaService.liberar(idReserva, cancelacionInput);
  }

  @Patch('/:idReserva')
  @Scopes('reservas:write')
    async update( @Param('idReserva', ParseIntPipe) idReserva: number, 
                  @Body() actualizacionInput: UpdateReservaDto): Promise<Reserva> {
    return this.reservaService.actualizar(idReserva, actualizacionInput);
  }

  @Get('/:idReserva')
  @Scopes('reservas:read')
  async consultarReserva(
    @Param('idReserva', ParseIntPipe) idReserva: number,
    @Query('usuarioId', ParseIntPipe) usuarioId: number
  ): Promise<Reserva> {
    return this.reservaService.consultarReserva(idReserva, usuarioId);
  }

  @Get('/')
  @Scopes('reservas:read')
  async consultarReservasDeUsuario( 
    @Query('usuarioId', ParseIntPipe) usuarioId: number, 
    @Query('page') page?: string, 
    @Query('limit') limit?: string,

    @Query('estado') estado?: 'confirmado' | 'pendiente' | 'cancelado', 
  ): Promise<PaginatedResponse<Reserva>> 
  {
    const pageNum = page ? parseInt(page) : undefined;
    const limitNum = limit ? parseInt(limit) : undefined; 

    return this.reservaService.consultarReservasDeUsuario(usuarioId, {
      page: pageNum, 
      limit: limitNum,
      estado
    });
  }
}