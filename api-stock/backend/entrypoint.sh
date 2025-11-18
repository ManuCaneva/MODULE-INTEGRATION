#!/bin/sh

echo "Ejecutando migraciones de la base de datos..."
npm run migration:run

echo "Iniciando aplicación..."
exec "$@"