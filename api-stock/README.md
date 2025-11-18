
# Sistema de Gestión de Productos y Stock

Una API RESTful desarrollada con NestJS para la gestión completa de productos, categorías y control de inventario con sistema de reservas.

## 📋 Prerrequisitos Mínimos
* Node.js (Descargar desde [Nodejs.org](https://nodejs.org/en/download))

* npm (viene con Node.js)

* Git (para clonar el repositorio)


## Instalación del proyecto

### 1. Clonar el repositorio
```
git clone <url-del-repositorio>
cd backend
```
### 2. Instalar dependencias
```
npm install
```
### 3. Configurar entorno
```
# Copiar archivo de configuración
cp .env.example .env
```
### 4. Crear y modificar variables de entorno

```
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=nombre_db

```
### 5. Ejecutar la aplicación

```
npm run start:dev

```

### 6. Cargar Datos de Prueba (Seeding)

Para poblar la base de datos con datos iniciales (categorías y productos de ejemplo), puedes ejecutar el siguiente comando desde el directorio `backend`:

```
npm run seed
```

Esto limpiará las tablas y cargará un conjunto de datos predefinido para facilitar el desarrollo y las pruebas.


## Ejecución con Docker

Para un despliegue rápido y consistente, se proporciona una configuración de Docker Compose que orquesta tanto la API como la base de datos PostgreSQL.

### Prerrequisitos
*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/) (generalmente incluido con Docker Desktop)

### Levantamiento de Servicios
1.  Asegúrese de que Docker se esté ejecutando en su sistema.
2.  Desde el directorio raíz del proyecto, ejecute el siguiente comando:
    ```shell
    docker compose up -d --build
    ```
    Este comando realizará las siguientes acciones:
    *   Construirá la imagen de la aplicación NestJS (`backend`) basándose en el `backend/Dockerfile`.
    *   Descargará la imagen de `postgres:15-alpine` para el servicio de base de datos (`db`).
    *   Creará e iniciará los contenedores para ambos servicios en modo desacoplado (`-d`).
    *   Las variables de entorno para la conexión a la base de datos se inyectan automáticamente desde `docker-compose.yml` al contenedor del backend.
    *   Se creará un volumen (`postgres-data`) para persistir los datos de la base de datos.

Una vez finalizado, el backend estará accesible en `http://localhost:3000` y el frontend en 'http://localhost:8000'.

Al iniciar, el contenedor del backend ejecuta automáticamente el script entrypoint.sh. Este script corre el comando npm run migration:run antes de iniciar la aplicación. Esto asegura que tu base de datos (stock_db) siempre tenga el esquema y las tablas más recientes.

### Seeding (Poblar la Base de Datos)
Este paso es manual y se hace una sola vez.

Después de que los contenedores estén corriendo y las tablas se hayan creado, debes ejecutar el script de seeding para poblar la base de datos con datos de prueba (categorías, productos, etc.).

Ejecuta el siguiente comando en tu terminal:
```
docker-compose exec backend npm run seed
```

### Detener los Servicios
Para detener y eliminar los contenedores, redes y volúmenes creados, ejecute:
```shell
docker-compose down
```

## Ingresar a la interfaz Swagger
```
http://localhost:3000/api
```

## Módulo de Autenticación (No implementado)

El módulo de autenticación se encargará de proteger los endpoints de la API. Actualmente, no está implementado.

## Módulo de Categorías

El módulo de categorías se encarga de gestionar las categorías de productos en el sistema.

### Endpoints

A continuación se describen los endpoints disponibles para el módulo de categorías:

- `GET /api/categorias`: Obtiene todas las categorías activas, ordenadas por nombre.
- `GET /api/categorias/:id`: Obtiene una categoría específica por su ID.
- `POST /api/categorias`: Crea una nueva categoría.
- `PATCH /api/categorias/:id`: Actualiza una categoría existente.
- `DELETE /api/categorias/:id`: Desactiva una categoría (borrado lógico).

## Módulo de Productos

El módulo de productos se encarga de gestionar los productos del sistema.

### Endpoints

A continuación se describen los endpoints disponibles para el módulo de productos:

- `GET /api/productos`: Obtiene todos los productos activos, con opción de paginación, búsqueda por nombre y filtro por categoría.
- `GET /api/productos/:id`: Obtiene un producto específico por su ID.
- `POST /api/productos`: Crea un nuevo producto.
- `PATCH /api/productos/:id`: Actualiza un producto existente.
- `DELETE /api/productos/:id`: Desactiva un producto (borrado lógico).

## Módulo de Reservas

El módulo de reservas se encarga de gestionar las reservas de stock de productos.

### Endpoints

A continuación se describen los endpoints disponibles para el módulo de reservas:

- `POST /api/reservas/reservar`: Crea una nueva reserva de stock para una lista de productos.
- `POST /api/reservas/liberar`: Libera el stock de una reserva existente.
- `GET /api/reservas/reservas/:idReserva`: Consulta el estado de una reserva específica.




