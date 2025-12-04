# Main - Configuración Principal de Django

## Responsabilidad

Este directorio contiene la **configuración central del proyecto Django**. Su responsabilidad es definir los ajustes globales, URLs principales, middleware, backends de autenticación y configuraciones de logging que aplican a toda la aplicación.

### Archivos Principales

- **settings.py**: Configuración global de Django (apps instaladas, middleware, bases de datos, APIs mock/reales, REST Framework, logging, email, Swagger).
- **urls.py**: Enrutamiento principal del proyecto. Define las URLs raíz y delega a las apps mediante `include()`.
- **backends.py**: Backend personalizado de autenticación por email (`EmailAuthBackend`) para permitir login con email en lugar de username.
- **middleware_request_id.py**: Middleware que asigna un ID único a cada request, registra tiempos de respuesta y captura excepciones no manejadas en los logs.
- **logging_filters.py**: Filtro de logging que inyecta `request_id` y `user_id` en cada log usando contexto thread-local.
- **wsgi.py**: Punto de entrada WSGI para servidores de producción.
- **asgi.py**: Punto de entrada ASGI para aplicaciones asíncronas (WebSockets, etc.).

### Funcionalidad

Este módulo centraliza la configuración del proyecto, permitiendo:

- Alternar entre APIs mock y reales mediante `USE_MOCK_APIS`.
- Configurar autenticación con `django-allauth` y modelo `Usuario` personalizado.
- Generar documentación automática de APIs con Swagger/OpenAPI (`drf-spectacular`).
- Rastrear requests con IDs únicos y contexto de usuario en los logs.
- Definir rutas globales hacia las apps de frontend y APIs internas.
