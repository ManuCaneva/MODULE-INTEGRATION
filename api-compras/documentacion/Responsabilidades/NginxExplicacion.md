# nginx - Proxy Reverso y Servidor Web

## Responsabilidad

Este directorio contiene la configuración de **Nginx** como proxy reverso para la aplicación Django. Su responsabilidad es recibir peticiones HTTP externas, reenviarlas a la aplicación Django y servir archivos estáticos/media de forma eficiente.

### Archivo Principal

- **nginx.conf**: Configuración del servidor Nginx que escucha en el puerto 8085 y actúa como proxy hacia Django en el puerto 8000.

### Funciones Principales

- **Proxy reverso**: Reenvía todas las peticiones a la aplicación Django (`django_app:8000`) preservando headers como `X-Real-IP`, `X-Forwarded-For` y `X-Forwarded-Proto`.
- **Servidor de archivos estáticos**: Sirve directamente archivos desde `/static/` y `/media/` sin pasar por Django, mejorando el rendimiento.
- **Seguridad**: Añade headers de seguridad (`X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`).
- **Soporte WebSockets**: Configurado para actualizar conexiones HTTP a WebSockets si la aplicación lo requiere.

### Integración

Nginx se ejecuta en un contenedor Docker delante de Django, manejando las peticiones públicas y distribuyendo la carga. En producción, HTTPS se maneja mediante el protocolo `X-Forwarded-Proto`.
