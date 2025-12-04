@echo off
setlocal ENABLEDELAYEDEXPANSION

REM ==== CONFIGURACIÓN BÁSICA ====
set IMAGE_NAME=ghcr.io/frre-ds/backend-compras-g04

echo ===============================
echo  Deploy de imagen Docker a GHCR
echo ===============================
echo.

REM 1) Verificar que no haya cambios sin commitear
git diff --quiet
if NOT "%ERRORLEVEL%"=="0" (
    echo Hay cambios sin commitear en el repositorio.
    echo Hace primero:
    echo   git add .
    echo   git commit -m "mensaje"
    echo y despues ejecuta este script.
    echo.
    pause
    exit /b 1
)

REM 2) Obtener el ultimo tag (o usar v1.0.0 si no hay ninguno)
FOR /F "delims=" %%v IN ('git describe --tags --abbrev=0 2^>nul') DO set LAST_TAG=%%v
if "%LAST_TAG%"=="" set LAST_TAG=v1.0.0

REM 3) Separar mayor.menor.patch (quitamos la 'v' del principio)
for /f "tokens=1-3 delims=." %%a in ("%LAST_TAG:~1%") do (
    set MAJOR=%%a
    set MINOR=%%b
    set PATCH=%%c
)

REM 4) Incrementar PATCH (v1.0.3 -> v1.0.4)
set /a PATCH=%PATCH%+1
set NEW_TAG=v%MAJOR%.%MINOR%.%PATCH%

echo Ultimo tag: %LAST_TAG%
echo Nuevo tag : %NEW_TAG%
echo.

REM 5) Confirmar
set /p OK=Continuar y construir/pushear esta version? (S/N): 
if /I NOT "%OK%"=="S" (
    echo Operacion cancelada.
    exit /b 0
)

REM 6) Construir la imagen local (igual que tu guia)
echo.
echo Construyendo imagen local "compras"...
docker build -t compras .
if NOT "%ERRORLEVEL%"=="0" (
    echo Error al construir la imagen.
    pause
    exit /b 1
)

REM 7) Taggear la imagen para GHCR: latest y la version
echo.
echo Taggeando imagen:
echo   %IMAGE_NAME%:latest
echo   %IMAGE_NAME%:%NEW_TAG%
docker tag compras %IMAGE_NAME%:latest
docker tag compras %IMAGE_NAME%:%NEW_TAG%

REM 8) Pushear ambas tags al registro
echo.
echo Pusheando imagen a GHCR...
docker push %IMAGE_NAME%:latest
if NOT "%ERRORLEVEL%"=="0" (
    echo Error al pushear tag latest.
    pause
    exit /b 1
)

docker push %IMAGE_NAME%:%NEW_TAG%
if NOT "%ERRORLEVEL%"=="0" (
    echo Error al pushear tag %NEW_TAG%.
    pause
    exit /b 1
)

REM 9) Crear y pushear el tag en git (opcional pero prolijo)
echo.
echo Creando tag en git: %NEW_TAG%
git tag %NEW_TAG%
git push origin %NEW_TAG%

echo.
echo ===============================================
echo  Listo! Imagen subida a:
echo    %IMAGE_NAME%:latest
echo    %IMAGE_NAME%:%NEW_TAG%
echo  y tag %NEW_TAG% creado en git.
echo ===============================================
echo.
pause
endlocal
