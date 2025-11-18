import { Module } from '@nestjs/common';
import { SeedsService } from './seeds.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Categoria } from '../../categorias/entities/categoria.entity';
import { Producto } from '../../productos/entities/producto.entity';
import { Reserva } from '../../reservas/entities/reserva.entity';
import { DetalleReserva } from '../../reservas/entities/detalle-reserva.entity';
import { ImagenProducto } from '../../productos/entities/imagen-producto.entity';
import { Dimensiones } from '../../productos/entities/dimensiones.entity';
import { UbicacionAlmacen } from '../../productos/entities/ubicacion-almacen.entity';

@Module({
  imports: [
    TypeOrmModule.forFeature([
      Categoria,
      Producto,
      Reserva,
      DetalleReserva,
      ImagenProducto,
      Dimensiones,
      UbicacionAlmacen,
    ]),
  ],
  providers: [SeedsService],
  exports: [SeedsService],
})
export class SeedsModule {}