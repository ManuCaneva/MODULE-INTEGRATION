import { IsString, IsNotEmpty, Matches, MaxLength, MinLength} from 'class-validator';

export class CreateUbicacionAlmacenDto {
  @IsString()
  @IsNotEmpty()
  street: string; 

  @IsString()
  @IsNotEmpty()
  city: string;

  @IsString()
  @IsNotEmpty()
  state: string;
  
  @IsString()
  @IsNotEmpty()
  @MinLength(2)
  @MaxLength(2)
  country: string;

  @IsString()
  @IsNotEmpty()
  @Matches(/^([A-Z]{1}\d{4}[A-Z]{3})$/)
  postalCode: string;
}