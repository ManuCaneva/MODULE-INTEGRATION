import { IsString, IsNotEmpty, MinLength } from 'class-validator';

export class CancelacionReservaInputDto {
  @IsString()
  @IsNotEmpty()
  @MinLength(5) // Capaz habría que agregar una longitud mínima para el motivo
  motivo: string;
}