import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ProductosModule } from './productos/productos.module';
import { CategoriasModule } from './categorias/categorias.module';
import { ReservasModule } from './reservas/reservas.module';
import { SeedsModule } from './database/seeds/seeds.module';
import { AuthModule } from './auth/auth.module';
import { TestAuthModule } from './auth/test-auth.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true, // Hace que el módulo esté disponible globalmente
      envFilePath: '.env', // Carga el archivo .env según el entorno
    }),
    TypeOrmModule.forRootAsync({
      useFactory: () => ({
        type: 'postgres',
        host: process.env.DB_HOST,
        port: process.env.DB_PORT ? parseInt(process.env.DB_PORT, 10) : 5432,
        username: process.env.DB_USERNAME,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME,
        entities: [__dirname + '/**/*.entity{.ts,.js}'],
        synchronize: process.env.NODE_ENV !== 'production',
      }),
    }),
    ProductosModule,
    CategoriasModule,
    ReservasModule,
    SeedsModule,
    AuthModule,
    TestAuthModule,
  ],
})
export class AppModule {}