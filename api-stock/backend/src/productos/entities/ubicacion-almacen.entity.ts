import { Entity, Column, PrimaryGeneratedColumn, OneToOne } from "typeorm";
import { Producto } from "./producto.entity";

@Entity('ubicacion_almacen')
export class UbicacionAlmacen {
    @PrimaryGeneratedColumn()
    id: number;

    @Column({ default: 'Sin especificar' })
    street: string;

    @Column()
    city: string;

    @Column()
    state: string;

    @Column({ name: 'postal_code' })
    postalCode: string;

    @Column()
    country: string;

    @OneToOne(() => Producto, producto => producto.ubicacion)
    producto: Producto;
}