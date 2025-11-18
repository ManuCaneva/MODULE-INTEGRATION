# Usar una imagen base de Node
FROM node:20-alpine

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
# Usamos 'ci' que es más rápido y seguro para entornos de CI/CD y Docker
RUN npm ci

# El comando para iniciar la aplicación será manejado por docker-compose
# para mayor flexibilidad. Dejamos el CMD por defecto o lo omitimos.
# Esto es intencional para que el hot-reloading funcione correctamente con volúmenes.
