import { IsNumber, IsPositive} from 'class-validator';

export class CreateDimensionesDto {
  @IsNumber()
  @IsPositive()
  largoCm: number;

  @IsNumber()
  @IsPositive()
  anchoCm: number;
  
  @IsNumber()
  @IsPositive()
  altoCm: number;
}