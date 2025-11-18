import { IsString, IsArray, ValidateNested, IsInt, Min, IsNotEmpty } from 'class-validator';
import { Type } from 'class-transformer';

class ProductoReservaDto {
  @IsInt()
  @Min(1)
  idProducto: number;

  @IsInt()
  @Min(1)
  cantidad: number;
}

export class ReservaInputDto {
  @IsString()
  @IsNotEmpty()
  idCompra: string;

  @IsInt()
  usuarioId: number;

  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => ProductoReservaDto)
  productos: ProductoReservaDto[];
}