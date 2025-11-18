# Dockerfile para el entorno de desarrollo del Frontend

FROM node:20-alpine

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Copiar package.json y package-lock.json (o npm-shrinkwrap.json)
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código fuente de la aplicación
COPY . .

# Exponer el puerto en el que se ejecuta la aplicación Next.js (por defecto 3000)
EXPOSE 8080

# Comando para iniciar la aplicación en modo de desarrollo
CMD ["npm", "run", "dev"]
