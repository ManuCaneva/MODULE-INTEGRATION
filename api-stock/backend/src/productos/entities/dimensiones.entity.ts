import { Entity, Column, OneToOne, PrimaryGeneratedColumn, JoinColumn} from "typeorm"
import { Producto } from "./producto.entity";

@Entity('dimensiones')
export class Dimensiones {
	@PrimaryGeneratedColumn()
	id: number; 

	@Column({type: 'float'})
	largoCm: number;

	@Column({type: 'float'})
	anchoCm: number;

	@Column({type: 'float'})
	altoCm: number;

	@OneToOne(() => Producto, producto => producto.dimensiones, {
		onDelete: 'CASCADE'
	})
	producto: Producto;
}