import os
import re
import logging
import requests
import docker

# Logger del proyecto (usa la configuración de Django en settings.LOGGING)
logger = logging.getLogger("app")

# v1.26.ventas  -> grupos: mayor=1, menor=26, slug='ventas'
TAG_PATTERN = re.compile(r"^v(\d+)\.(\d+)\.([\w-]+)$")


# ---------------------------------------------------------------------------
# 1) Autenticación y obtención del token JWT de Docker Hub
# ---------------------------------------------------------------------------
def obtener_token_dockerhub(usuario: str, contrasena: str) -> str:
    """
    Devuelve un token JWT para llamar a la API de Docker Hub.
    """
    url_login = "https://hub.docker.com/v2/users/login/"
    resp = requests.post(
        url_login,
        json={"username": usuario, "password": contrasena},
        timeout=10,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Login a Docker Hub falló: {resp.text}")
    return resp.json()["token"]


# ---------------------------------------------------------------------------
# 2) Leer el último tag y calcular el siguiente
# ---------------------------------------------------------------------------
def obtener_siguiente_version(
    usuario: str,
    repo: str,
    slug: str,
    contrasena: str,
) -> str:
    """
    Consulta todos los tags del repositorio (privado o público), detecta
    para el identificador dado el mayor con formato v<mayor>.<menor>.<slug>
    y devuelve el siguiente (menor + 1).
    """
    token = obtener_token_dockerhub(usuario, contrasena)
    headers = {"Authorization": f"JWT {token}"}
    url = f"https://hub.docker.com/v2/repositories/{usuario}/{repo}/tags?page_size=100"

    mayor, menor = -1, -1
    logger.info("📡 Consultando tags remotos en Docker Hub…")

    while url:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            raise RuntimeError(f"No se pudieron obtener los tags: {r.text}")
        data = r.json()

        # Analizar cada tag
        for result in data.get("results", []):
            tag_name = result.get("name", "")
            m = TAG_PATTERN.match(tag_name)
            if m and m.group(3) == slug:
                may, men, _ = m.groups()
                may = int(may)
                men = int(men)
                if may > mayor or (may == mayor and men > menor):
                    mayor, menor = may, men

        # Paginación
        url = data.get("next")

    # Ningún tag => comenzamos en v1.00.<slug>
    if mayor == -1:
        logger.warning(
            "⚠️  No se encontraron tags 'vX.Y.%s'; se usará v1.00.%s.",
            slug, slug
        )
        return f"v1.00.{slug}"

    siguiente = f"v{mayor}.{menor + 1:02d}.{slug}"
    logger.info(
        "🔖 Último tag: v%d.%02d.%s → Nuevo tag: %s",
        mayor, menor, slug, siguiente
    )
    return siguiente


# ---------------------------------------------------------------------------
# 3) Construir y subir la imagen
# ---------------------------------------------------------------------------
def construir_y_subir_imagen(
    directorio_proyecto: str,
    nombre_repo: str,
    identificador: str,
    dockerhub_usuario: str,
    dockerhub_contrasena: str,
):
    """
    Construye y sube la nueva imagen con tag auto-incrementado.
    Tag: 'vX.Y.<identificador>'
    Repo/tag final: '{dockerhub_usuario}/{nombre_repo}:vX.Y.<identificador>'
    """
    # 3.1 Calcular el próximo tag
    tag_nuevo = obtener_siguiente_version(
        dockerhub_usuario,
        nombre_repo,
        identificador,
        dockerhub_contrasena,
    )
    etiqueta_imagen = f"{dockerhub_usuario}/{nombre_repo}:{tag_nuevo}"

    # 3.2 Login local + build
    try:
        cliente_docker = docker.from_env()

        logger.info("🔐 'docker login' local…")
        cliente_docker.login(
            username=dockerhub_usuario,
            password=dockerhub_contrasena
        )
        logger.info("✅ Login local exitoso.")

        logger.info("🛠️  Construyendo %s…", etiqueta_imagen)
        build_output = cliente_docker.api.build(
            path=directorio_proyecto,
            tag=etiqueta_imagen,
            dockerfile="Dockerfile",
            rm=True,
            decode=True,
        )

        for entry in build_output:  # cada dict del stream de build
            try:
                if "stream" in entry:
                    msg = (entry.get("stream") or "").strip()
                    if msg:
                        logger.info(msg)
                elif "error" in entry:
                    # error en el build
                    raise RuntimeError((entry.get("error") or "").strip())
            except Exception as e:
                logger.warning("Línea de build inesperada: %r (err=%s)", entry, e)

        logger.info("🏁 Build completado.")

    except Exception as e:
        logger.error("❌ Error durante el build: %s", e)
        return

    # 3.3 Push
    try:
        logger.info("☁️  Pusheando %s…", etiqueta_imagen)
        push_output = cliente_docker.images.push(
            etiqueta_imagen,
            stream=True,
            decode=True,
        )

        for entry in push_output:
            if "status" in entry and "id" in entry:
                layer = entry.get("id")
                status = entry.get("status")
                progress = entry.get("progress", "")
                logger.debug("⏳ %s: %s %s", layer, status, progress)
            elif "status" in entry:
                logger.info("🔄 %s", entry.get("status"))
            elif "errorDetail" in entry:
                # error en el push
                raise RuntimeError(entry["errorDetail"]["message"])

        logger.info("✅ Imagen subida correctamente.")

    except Exception as e:
        logger.error("❌ Error al subir la imagen: %s", e)


# ---------------------------------------------------------------------------
# 4) Ejecutar como script (ejemplo)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Recomendación: usar variables de entorno para credenciales
    # DOCKERHUB_USER / DOCKERHUB_PASS
    usuario = os.getenv("DOCKERHUB_USER", "TU_USUARIO")
    password = os.getenv("DOCKERHUB_PASS", "TU_PASSWORD")

    construir_y_subir_imagen(
        directorio_proyecto=r"D:\Users\MAXIMO\Documents\programas\proyectosDjango\TiendaSoftware",
        nombre_repo="django-app",
        identificador="software",
        dockerhub_usuario=usuario,
        dockerhub_contrasena=password,  # Ideal: PAT si tenés 2FA
    )
