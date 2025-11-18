import { Entity, Column, PrimaryGeneratedColumn, ManyToMany, JoinTable, OneToMany, OneToOne, JoinColumn } from 'typeorm';
import { Categoria } from '../../categorias/entities/categoria.entity';
import { ImagenProducto } from './imagen-producto.entity';
import { Dimensiones } from './dimensiones.entity';
import { UbicacionAlmacen } from './ubicacion-almacen.entity';

@Entity('productos')
export class Producto {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ length: 200 })
  nombre: string;

  @Column({ type: 'text', nullable: true })
  descripcion: string;

  @Column({ type: 'float' })
  precio: number;

  @Column({ name: 'stock_disponible', default: 0 })
  stockDisponible: number;

  @OneToOne(() => Dimensiones, dimensiones => dimensiones.producto, {cascade: true})
  @JoinColumn()
  dimensiones: Dimensiones;

  @OneToOne(() => UbicacionAlmacen, ubicacion => ubicacion.producto, {cascade: true})
  @JoinColumn()
  ubicacion: UbicacionAlmacen;

  @Column({ name: 'peso_kg', type: 'float', nullable: true })
  pesoKg: number;

  @OneToMany(() => ImagenProducto, imagen => imagen.producto, { cascade: true })
  imagenes: ImagenProducto[];

  @ManyToMany(() => Categoria, categoria => categoria.productos, { cascade: true })
  @JoinTable({
    name: 'producto_categorias',
    joinColumn: { name: 'producto_id', referencedColumnName: 'id' },
    inverseJoinColumn: { name: 'categoria_id', referencedColumnName: 'id' }
  })
  categorias: Categoria[];
}