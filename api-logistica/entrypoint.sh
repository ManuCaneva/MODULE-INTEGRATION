#!/bin/bash
set -e # Falla si algo sale mal

DB_HOST="db"  # Asumiendo que tu servicio de DB se llama 'db' en docker-compose
DB_PORT="3306"

echo "API -> Esperando que la base de datos ($DB_HOST:$DB_PORT) esté disponible..."

# Bucle que usa netcat (nc) para verificar si el puerto está abierto
until nc -z "$DB_HOST" "$DB_PORT"; do
  echo "La base de datos no está lista, reintentando en 1 segundo..."
  sleep 1
done

echo "¡Base de datos lista!"

# --- ¡NUEVO! ---
# Limpiamos los saltos de línea de Windows (\r) de TODOS los archivos CSV
# antes de que la aplicación C# intente leerlos.
echo "Limpiando saltos de línea de Windows de los archivos CSV..."
for file in /app/csvs/*.csv; do
  # Comprobamos si el archivo existe antes de intentar limpiarlo
  if [ -f "$file" ]; then
    sed -i 's/\r$//' "$file"
  fi
done
echo "Limpieza de CSVs completada."
# --- FIN DEL BLOQUE NUEVO ---

echo "Iniciando la aplicación..."

# Ejecuta la aplicación de .NET
exec dotnet ApiDePapas.dll