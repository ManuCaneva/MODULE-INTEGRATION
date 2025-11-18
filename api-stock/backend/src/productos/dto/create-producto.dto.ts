import { IsString, IsNumber, IsArray, IsOptional, IsUrl, Min, IsPositive, ArrayNotEmpty, IsInt, IsNotEmpty, ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';
import { CreateDimensionesDto } from './create-dimensiones.dto';
import { CreateUbicacionAlmacenDto } from './create-ubicacion-almacen.dto';

export class CreateProductoDto {
  @IsString()
  nombre: string;

  @IsString()
  @IsOptional()
  descripcion?: string;

  @IsNumber()
  @Min(0)
  precio: number;

  @IsNumber()
  @IsPositive()
  stockInicial: number;

  @IsNumber()
  @Min(0)
  @IsOptional()
  pesoKg?: number;

  @IsNotEmpty()
  @ValidateNested()
  @Type(() => CreateDimensionesDto)
  dimensiones: CreateDimensionesDto;

  @IsNotEmpty()
  @ValidateNested()
  @Type(() => CreateUbicacionAlmacenDto)
  ubicacion: CreateUbicacionAlmacenDto;

  @IsArray()
  @IsUrl({}, { each: true })
  @IsOptional()
  imagenes?: string[];

  @IsArray()
  @IsOptional()
  @ArrayNotEmpty()
  @IsInt({ each: true })
  categoriaIds?: number[];
}