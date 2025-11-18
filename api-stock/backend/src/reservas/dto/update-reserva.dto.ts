import { IsString, IsNotEmpty, IsInt, IsEnum } from "class-validator";

export class UpdateReservaDto {
  @IsInt()
  usuarioId: number;

  @IsString()
  @IsNotEmpty()
  @IsEnum(['confirmado', 'pendiente', 'cancelado'])
  estado: 'confirmado' | 'pendiente' | 'cancelado';
}