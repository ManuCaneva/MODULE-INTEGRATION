"""Cliente HTTP especializado para la API de productos.

Este módulo define :class:`ProductoAPIClient`, una implementación que
hereda del cliente base ubicado en ``utils.apiCliente.base``. La idea es
centralizar toda la comunicación HTTP con la API de productos expuesta
por este proyecto. De esta forma, cuando sea necesario redirigir el
cliente hacia otro servicio con la misma interfaz, bastará con ajustar
la configuración del ``base_url`` sin modificar el resto del código que
consume estos recursos.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Callable

from django.conf import settings

from utils.apiCliente.base import BaseAPIClient
from utils.keycloak import get_service_token_provider


class ProductoAPIClient(BaseAPIClient):
    """Cliente concreto para interactuar con la API de productos.

    El contrato implementado por esta clase replica los endpoints
    disponibles en ``apps.apis.productoApi.views.ProductoViewSet``:

    - ``GET /productos/``         → :meth:`listar_productos`
    - ``GET /productos/{id}/``    → :meth:`obtener_producto`

    Parameters
    ----------
    base_url:
        URL base del servicio. Si no se especifica, se utiliza la
        configuración declarada en :mod:`Main.settings`.
    timeout:
        Tiempo máximo de espera por respuesta HTTP.
    max_retries:
        Número máximo de reintentos ante fallos de conexión o timeout.
    token / api_key:
        Credenciales opcionales para enviar en cada solicitud.
    token_provider:
        Callable opcional que entrega un JWT fresco (por ejemplo, desde Keycloak).
    use_service_token:
        Si es ``True`` y la configuración incluye credenciales de servicio,
        el cliente solicitará tokens ``client_credentials`` automáticamente.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        *,
        timeout: float = 8.0,
        max_retries: int = 2,
        token: Optional[str] = None,
        api_key: Optional[str] = None,
        token_provider: Optional[Callable[[], str]] = None,
        use_service_token: bool = False,
    ) -> None:
        base_por_defecto = getattr(
            settings,
            "PRODUCTOS_API_BASE_URL",
            getattr(settings, "SITE_URL", "http://localhost:8000"),
        )
        if base_url is None:
            base_url = base_por_defecto

        if use_service_token and token_provider is None:
            token_provider = get_service_token_provider(silent=True)

        super().__init__(
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            token=token,
            api_key=api_key,
            token_provider=token_provider,
        )

    # ------------------------------------------------------------------
    # Endpoints principales de la API de productos
    # ------------------------------------------------------------------
    def listar_productos(
        self,
        *,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
        categoria: Optional[str] = None,
        marca: Optional[str] = None,
    ) -> Any:
        """Obtiene el listado paginado de productos disponibles."""
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if search:
            params["search"] = search
        if categoria:
            params["categoria"] = categoria
        if marca:
            params["marca"] = marca

        return self.get("/api/product/", params=params or None, expected_status=200)

    def obtener_producto(self, producto_id: int, *, parametros_extra: Optional[Dict[str, Any]] = None) -> Any:
        """Recupera el detalle de un producto específico."""
        params = parametros_extra if parametros_extra else None
        return self.get(f"/productos/{producto_id}/", params=params, expected_status=200)

    def listar_categorias(self) -> Any:
        """Obtiene el listado de categorías disponibles desde la API de Stock."""
        return self.get("/api/category/", expected_status=200)


def obtener_cliente_productos(**kwargs: Any) -> ProductoAPIClient:
    """Helper para instanciar ``ProductoAPIClient`` usando la configuración del proyecto."""
    base_url = getattr(settings, "PRODUCTOS_API_BASE_URL", "http://localhost:8000") 
    kwargs.setdefault("use_service_token", True)
    
    return ProductoAPIClient(base_url=base_url, **kwargs)
