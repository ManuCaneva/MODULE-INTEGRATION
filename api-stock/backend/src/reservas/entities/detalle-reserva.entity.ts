import { Entity, Column, PrimaryGeneratedColumn, ManyToOne, JoinColumn } from 'typeorm';
import { Reserva } from './reserva.entity';
import { Producto } from '../../productos/entities/producto.entity';

@Entity('detalles_reserva')
export class DetalleReserva {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  cantidad: number;

  @ManyToOne(() => Reserva, reserva => reserva.detalles, {
    onDelete: 'CASCADE'
  })
  @JoinColumn({ name: 'reserva_id' })
  reserva: Reserva;

  @Column({ name: 'reserva_id' })
  reservaId: number;

  @ManyToOne(() => Producto)
  @JoinColumn({ name: 'producto_id' })
  producto: Producto;

  @Column({ name: 'producto_id' })
  productoId: number;
}