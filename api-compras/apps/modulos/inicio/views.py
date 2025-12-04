from django.shortcuts import render
import logging
from time import perf_counter
from apps.apis.productoApi.client import ProductoAPIClient, obtener_cliente_productos
from utils.apiCliente.stock import StockClient
from django.conf import settings
import unicodedata

logger = logging.getLogger(__name__)

import unicodedata, re

def normalize(text):
    if not text:
        return ""
    # convertir todo a string siempre
    text = str(text)

    # eliminar caracteres invisibles
    text = (
        text.replace("\u00a0", " ")   # NO-BREAK SPACE
            .replace("\u200b", "")   # ZERO WIDTH SPACE
            .replace("\u200c", "")
            .replace("\u200d", "")
            .replace("\ufeff", "")
            .strip()
    )

    # bajar a minúsculas
    text = text.lower()

    # normalizar tildes
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")

    # colapsar múltiples espacios
    text = re.sub(r"\s+", " ", text)

    return text


def inicio_view(request):
    """Obtiene productos desde la API de Stock (sin datos hardcodeados)."""
    logger.info("inicio_view llamada: user=%s path=%s", getattr(request, "user", None), request.get_full_path())

    # parámetros de filtros y paginación
    termino_busqueda = request.GET.get("busqueda", "").strip()
    categoria_filtrada = request.GET.get("categoria", "").strip()
    marca_filtrada = request.GET.get("marca", "").strip()
    precio_minimo = request.GET.get("precio_minimo", "").strip()
    precio_maximo = request.GET.get("precio_maximo", "").strip()
    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except Exception:
        page = 1
    try:
        limit = int(request.GET.get("limit", 18))
        if limit < 1:
            limit = 18
    except Exception:
        limit = 18

    productos = []
    pagination_context = {}
    start = perf_counter()
    try:
        client = obtener_cliente_productos()
        
        logger.debug("Llamando a StockClient.listar_productos con limit=5000 para obtener todos los resultados filtrados=%s", {
            "busqueda": termino_busqueda,
            "categoria": categoria_filtrada,
            "marca": marca_filtrada,
        })
        
        # Una sola llamada: traer muchos productos para aplicar filtros y paginar localmente
        resultado = client.listar_productos(
            page=1, 
            limit=5000,
            search=termino_busqueda,
        )
        

        elapsed = perf_counter() - start
        logger.info("Stock API listar_productos respondió en %.3fs", elapsed)
        if isinstance(resultado, dict) and "data" in resultado:
            productos_raw = resultado.get("data") or []
        else:
            if resultado is None:
                logger.warning("Stock API devolvió None en listar_productos")
            elif not isinstance(resultado, list):
                logger.warning("Formato inesperado de respuesta de Stock API: %s", type(resultado))
            productos_raw = resultado or []

        for p in productos_raw:
            # Debug: mostrar estructura del primer producto
            if productos_raw.index(p) == 0:
                logger.debug("Estructura del primer producto raw: %s", p)
            
            categoria = None
            # El campo viene como 'categorias' (plural) y es una lista
            categorias_list = p.get("categorias", [])
            if categorias_list and isinstance(categorias_list, list) and len(categorias_list) > 0:
                # Tomar la primera categoría de la lista
                primera_cat = categorias_list[0]
                if isinstance(primera_cat, dict):
                    categoria = primera_cat.get("nombre")
                elif isinstance(primera_cat, str):
                    categoria = primera_cat
            
            # Fallback: intentar con campo singular 'categoria'
            if not categoria:
                if isinstance(p.get("categoria"), dict):
                    categoria = p["categoria"].get("nombre")
                else:
                    categoria = p.get("categoria_nombre") or p.get("categoria")

            # Obtener imagen principal de la lista de imágenes
            imagenes_list = p.get("imagenes", [])
            imagen = ""
            
            if imagenes_list:
                if isinstance(imagenes_list, dict):
                    # Si es un solo diccionario, extraer la URL directamente
                    imagen = imagenes_list.get("url", "")
                elif isinstance(imagenes_list, list):
                    # Si es una lista, buscar la imagen marcada como principal
                    for img in imagenes_list:
                        if isinstance(img, dict) and img.get("esPrincipal"):
                            imagen = img.get("url", "")
                            break
                    # Si no hay principal, tomar la primera imagen disponible
                    if not imagen and len(imagenes_list) > 0:
                        primera_img = imagenes_list[0]
                        if isinstance(primera_img, dict):
                            imagen = primera_img.get("url", "")
                            print("esto es la url de la imagen", imagen)

            precio = p.get("precio")
            try:
                precio = float(precio) if precio is not None else 0.0
            except Exception:
                logger.debug("Precio inválido para producto id=%s precio_raw=%s", p.get("id") or p.get("pk"), p.get("precio"))
                precio = 0.0

            productos.append({
                "id": p.get("id") or p.get("pk"),
                "nombre": p.get("nombre") or p.get("title") or "",
                "descripcion": p.get("descripcion") or p.get("description") or "",
                "precio": precio,
                "categoria": categoria or "",
                "marca": p.get("marca") or "",
                "imagen": imagen or "",
            })
        logger.info("Obtenidos %d productos (raw=%d) desde Stock API", len(productos), len(productos_raw))
        # Log para debug: mostrar categorías únicas en los productos
        categorias_en_productos = {p.get("categoria", "") for p in productos if p.get("categoria", "")}
        logger.debug("Categorías encontradas en productos: %s", sorted(categorias_en_productos))
    except Exception as e:
        logger.exception("Error obteniendo productos desde Stock API para path=%s user=%s: %s", request.get_full_path(), getattr(request, "user", None), e)
        productos = []

    # Obtener categorías desde la API de Stock usando StockClient
    categorias_disponibles = []
    try:
        stock_client = StockClient(base_url=settings.STOCK_API_BASE_URL)
        resultado_categorias = stock_client.listar_categorias()
        logger.debug("Respuesta de categorías desde Stock: %s", resultado_categorias)
        
        if isinstance(resultado_categorias, list):
            categorias_raw = resultado_categorias
        elif isinstance(resultado_categorias, dict) and "data" in resultado_categorias:
            categorias_raw = resultado_categorias.get("data") or []
        else:
            categorias_raw = []
        
        # Extraer nombres de categorías
        for cat in categorias_raw:
            if isinstance(cat, dict):
                nombre = cat.get("nombre") or cat.get("name") or cat.get("title")
                if nombre:
                    categorias_disponibles.append(nombre)
            elif isinstance(cat, str):
                categorias_disponibles.append(cat)
        
        categorias_disponibles = sorted(set(categorias_disponibles))
        logger.info("Obtenidas %d categorías desde Stock API", len(categorias_disponibles))
    except Exception as e:
        logger.exception("Error obteniendo categorías desde Stock API: %s", e)
        # Fallback: extraer categorías de los productos si falla la API
        categorias_disponibles = sorted({p.get("categoria", "") for p in productos if p.get("categoria", "")})

    # Extraer marcas disponibles de los productos
    marcas_disponibles = sorted({p.get("marca", "") for p in productos if p.get("marca", "")})

    # =============================
    #     FILTROS CON NORMALIZE
    # =============================

    q = normalize(termino_busqueda)
    cat_f = normalize(categoria_filtrada)
    marca_f = normalize(marca_filtrada)

    logger.debug("Categoría filtrada (normalizada): '%s' (original: '%s')", cat_f, categoria_filtrada)
    if productos and cat_f:
        # Log de ejemplo: primera categoría de producto
        ejemplo_cat = normalize(productos[0].get("categoria", ""))
        logger.debug("Ejemplo categoría de producto (normalizada): '%s' (original: '%s')", 
                    ejemplo_cat, productos[0].get("categoria", ""))

    def _filtrar(prod):
        nombre = normalize(prod.get("nombre", ""))        
        marca = normalize(prod.get("marca", ""))
        categoria = normalize(prod.get("categoria", ""))

        # búsqueda general
        if q and (q not in nombre and q not in marca):
            return False

        # categoría
        if cat_f and cat_f != categoria:
            return False

        # marca
        if marca_f and marca_f != marca:
            return False

        # precio
        try:
            precio = prod.get("precio", 0)
            if precio_minimo and float(precio_minimo) > precio:
                return False
            if precio_maximo and float(precio_maximo) < precio:
                return False
        except:
            pass

        return True

    productos = [p for p in productos if _filtrar(p)]

    # Paginación manual después de filtrar
    total_resultados = len(productos)
    per_page = limit  # 18 productos por página
    total_pages = max(1, (total_resultados + per_page - 1) // per_page) if total_resultados > 0 else 1
    
    # Validar página
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    # Calcular índices para slice
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    productos_pagina = productos[start_idx:end_idx]
    
    pagination_context = {
        "total": total_resultados,
        "per_page": per_page,
        "current_page": page,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "next_page": page + 1 if page < total_pages else None,
        "prev_page": page - 1 if page > 1 else None,
    }

    logger.debug(
        "Filtros aplicados: busqueda=%s categoria=%s marca=%s precio_min=%s precio_max=%s -> %d resultados (página %d de %d)",
        termino_busqueda, categoria_filtrada, marca_filtrada, precio_minimo, precio_maximo, total_resultados, page, total_pages
    )

    carrito = []
    total_carrito = 0.0

    context = {
        "productos": productos_pagina,
        "categorias": categorias_disponibles,
        "marcas": marcas_disponibles,
        "filtros": {
            "busqueda": termino_busqueda,
            "categoria": categoria_filtrada,
            "marca": marca_filtrada,
            "precio_minimo": precio_minimo,
            "precio_maximo": precio_maximo,
        },
        "cantidad_resultados": total_resultados,
        "carrito": carrito,
        "total_carrito": total_carrito,
        "pagination": pagination_context,
    }

    logger.info("Renderizando inicio.html con %d productos de %d totales (página %d de %d)", len(productos_pagina), total_resultados, page, total_pages)
    return render(request, "inicio.html", context)
