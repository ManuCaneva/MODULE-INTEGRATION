@echo off
setlocal

echo [1/3] Deteniendo contenedores y limpiando volumenes...
docker compose down --volumes
if errorlevel 1 goto :error

echo [2/3] Construyendo imagenes...
docker compose build
if errorlevel 1 goto :error

echo [3/3] Levantando servicios en segundo plano...
docker compose up -d
if errorlevel 1 goto :error

echo Docker Compose levantado correctamente.
goto :eof

:error
echo.
echo [ERROR] Ocurrio un problema al ejecutar Docker Compose. Revisa los mensajes anteriores.
exit /b 1
