import { IsString, IsOptional, MinLength, MaxLength } from 'class-validator';

export class CreateCategoriaDto {
  @IsString()
  @MinLength(1)
  @MaxLength(100)
  nombre: string;

  @IsString()
  @IsOptional()
  descripcion?: string;
}