# Guía para subir una imagen Docker al registro de la cátedra (GHCR)

### Este documento explica los pasos necesarios para construir y publicar una imagen Docker en el GitHub Container Registry (GHCR) utilizado por la cátedra.

1. Autenticación en Docker

    Antes de realizar el push al registro, es necesario autenticarse en ghcr.io utilizando un token personal de GitHub.

    Ingresar a la página de creación de tokens:
    https://github.com/settings/tokens

    Crear un Personal Access Token (Classic) con:

    - Expiration: 90 days

    - Scopes habilitados:
        - write:packages
        - read:packages

    - bEjecutar el login en Docker:

     docker login ghcr.io
        - Usuario: tu usuario de GitHub
        - Contraseña: el token generado en GitHub

2. Construir la imagen Docker

    Desde la carpeta donde se encuentra el Dockerfile, ejecutar:

    docker build -t compras .

    Esto crea una imagen local llamada compras.

3. Asignar el tag correspondiente al registro de la cátedra

    Se debe taggear la imagen con el nombre oficial del grupo:

    docker tag compras ghcr.io/frre-ds/backend-compras-g04:latest

    Este será el nombre final con el que se publicará la imagen.

4. Subir la imagen al registro GHCR

    Finalmente, ejecutar:

    docker push ghcr.io/frre-ds/backend-compras-g04:latest

## Una vez finalizado el proceso, la imagen estará disponible en la sección Packages de la organización FRRe-DS en GitHub.