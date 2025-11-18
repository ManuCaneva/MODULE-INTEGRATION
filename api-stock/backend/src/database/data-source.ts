import { DataSource, DataSourceOptions } from 'typeorm';
import * as dotenv from 'dotenv';
import * as path from 'path';

// Cargar variables de entorno (del archivo .env)
dotenv.config();

// Definir las opciones de la base de datos
export const dataSourceOptions: DataSourceOptions = {
  type: 'postgres',
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432', 10),
  username: process.env.DB_USERNAME || 'user',
  password: process.env.DB_PASSWORD || 'password',
  database: process.env.DB_NAME || 'stock_db',

  // IMPORTANTE:
  // Usar __dirname + '...' asegura que las rutas funcionen
  // tanto en desarrollo (.ts) como en producción (.js en dist/)
  entities: [path.join(__dirname, '/../**/*.entity{.ts,.js}')],
  migrations: [path.join(__dirname, '/migrations/*{.ts,.js}')],

  // Nunca usar 'synchronize: true' en producción con migraciones
  synchronize: false,
};

// Exportar la instancia de DataSource
const dataSource = new DataSource(dataSourceOptions);
export default dataSource;