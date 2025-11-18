# Documentación del Proyecto

Este proyecto es una API de gestión de stock de bienes y servicios, desarrollada con NestJS. Proporciona endpoints para gestionar productos, categorías y reservas de stock.

## Cómo ejecutar el proyecto

1. Clonar el repositorio.
2. Instalar las dependencias con `npm install`.
3. Configurar las variables de entorno en un archivo `.env` (ver `.env.example` para un ejemplo).
4. Ejecutar las migraciones de la base de datos (si las hay).
5. Iniciar el servidor con `npm run start:dev`.

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
