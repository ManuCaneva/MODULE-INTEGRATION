import { Entity, Column, PrimaryGeneratedColumn, OneToMany } from 'typeorm';
import { DetalleReserva } from './detalle-reserva.entity';

@Entity('reservas')
export class Reserva {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ name: 'id_compra', unique: true })
  idCompra: string;

  @Column()
  usuarioId: number;

  @Column({ 
    type: 'enum', 
    enum: ['confirmado', 'pendiente', 'cancelado'],
    default: 'pendiente'
  })
  estado: string;

  @Column({ name: 'expires_at', type: 'timestamp' })
  expiresAt: Date;

  @Column({ name: 'fecha_creacion', type: 'timestamp', default: () => 'CURRENT_TIMESTAMP' })
  fechaCreacion: Date;

  @Column({ name: 'fecha_actualizacion', type: 'timestamp', default: () => 'CURRENT_TIMESTAMP', onUpdate: 'CURRENT_TIMESTAMP' })
  fechaActualizacion: Date;

  @OneToMany(() => DetalleReserva, detalle => detalle.reserva, { cascade: true })
  detalles: DetalleReserva[];
}
