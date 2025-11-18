import { Entity, Column, PrimaryGeneratedColumn, ManyToOne, JoinColumn } from 'typeorm';
import { Producto } from './producto.entity';

@Entity('imagenes_producto')
export class ImagenProducto {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'text' })
  url: string;

  @Column({ name: 'es_principal', default: false })
  esPrincipal: boolean;

  @ManyToOne(() => Producto, producto => producto.imagenes, {
    onDelete: 'CASCADE'
  })
  @JoinColumn({ name: 'producto_id' })
  producto: Producto;

  @Column({ name: 'producto_id' })
  productoId: number;
}