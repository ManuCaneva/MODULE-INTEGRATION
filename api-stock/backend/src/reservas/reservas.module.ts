import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ReservaController } from './reservas.controller';
import { ReservasService } from './reservas.service';
import { Reserva } from './entities/reserva.entity';
import { DetalleReserva } from './entities/detalle-reserva.entity';
import { ProductosModule } from '../productos/productos.module';

@Module({
  imports: [
    TypeOrmModule.forFeature([Reserva, DetalleReserva]),
    ProductosModule,
  ],
  controllers: [ReservaController],
  providers: [ReservasService],
  exports: [ReservasService],
})
export class ReservasModule {}