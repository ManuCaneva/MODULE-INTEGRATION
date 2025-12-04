"""Cliente HTTP para interactuar con el servicio de carrito (aCarrito).

Este módulo expone una clase especializada que hereda del cliente base
ubicado en ``utils.apiCliente``. La clase encapsula todas las
operaciones que ofrece la API de carrito, de forma que el resto del
código de Django pueda permanecer desacoplado de los detalles de
comunicación HTTP. El objetivo es que, cuando se redirija el tráfico
hacia otra implementación compatible de la API, el cambio se limite a la
configuración del ``base_url`` sin tener que ajustar las vistas ni los
serializadores.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Callable

from django.conf import settings

from utils.apiCliente.base import BaseAPIClient
from utils.apiCliente.stock import StockClient
from utils.keycloak import get_service_token_provider


class CarritoAPIClient(BaseAPIClient):
    """Cliente concreto para la API de carrito (aCarrito).

    El contrato que implementa este cliente está basado en el conjunto de
    endpoints expuestos por nuestra API interna de carrito:

    - ``GET    /shopcart/``               → :meth:`obtener_carrito`
    - ``POST   /shopcart/``               → :meth:`agregar_producto`
    - ``PUT    /shopcart/{productId}/``   → :meth:`actualizar_producto`
    - ``DELETE /shopcart/{productId}/``   → :meth:`eliminar_producto`
    - ``DELETE /shopcart/``               → :meth:`vaciar_carrito`
    - ``PUT    /shopcart/``               → :meth:`sincronizar_carrito`

    Además, se exponen utilidades para recuperar información de los
    productos asociados al carrito reutilizando el ``StockClient``.
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
        stock_client: Optional[StockClient] = None,
    ) -> None:
        # establecer URL base por defecto desde la configuración de Django (setting estimado setting)
        base_por_defecto = getattr(settings, "base_url_api", "http://localhost:8000/api/")
        if base_url is None:
            base_url = getattr(settings, "CARRITO_API_BASE_URL", base_por_defecto) or base_por_defecto

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

        if stock_client is None:
            stock_base = (
                getattr(settings, "STOCK_API_BASE_URL", None)
                or getattr(settings, "STOCK_API_BASE", None)
                or base_por_defecto
            )
            stock_token_provider = token_provider if token_provider else (
                get_service_token_provider(silent=True) if use_service_token else None
            )
            stock_client = StockClient(base_url=stock_base, token_provider=stock_token_provider)
        self.stock_client = stock_client

    # ------------------------------------------------------------------
    # Endpoints principales del servicio de carrito
    # ------------------------------------------------------------------
    def obtener_carrito(self, usuario_id: int) -> Dict[str, Any]:
        """Obtiene el carrito activo del usuario indicado."""
        params = {"usuarioId": usuario_id}
        return self.get("/shopcart/", params=params, expected_status=200)

    def obtener_items(self, usuario_id: int) -> List[Dict[str, Any]]:
        """Devuelve únicamente los ítems del carrito para un usuario."""
        carrito = self.obtener_carrito(usuario_id)
        if isinstance(carrito, dict):
            items = carrito.get("items", [])
            return items if isinstance(items, list) else []
        return []

    def agregar_producto(self, usuario_id: int, producto_id: int, cantidad: int = 1) -> Dict[str, Any]:
        """Agrega un producto al carrito del usuario."""
        payload = {"usuarioId": usuario_id, "productId": producto_id, "quantity": int(cantidad)}
        return self.post("/shopcart/", json=payload, expected_status=(200, 201))

    def actualizar_producto(self, usuario_id: int, producto_id: int, cantidad: int) -> Dict[str, Any]:
        """Actualiza la cantidad de un producto específico."""
        payload = {"usuarioId": usuario_id, "quantity": int(cantidad)}
        return self.put(f"/shopcart/{producto_id}/", json=payload, expected_status=(200, 204))

    def eliminar_producto(self, usuario_id: int, producto_id: int) -> Any:
        """Elimina un producto del carrito del usuario."""
        payload = {"usuarioId": usuario_id}
        return self.request("DELETE", f"/shopcart/{producto_id}/", json=payload, expected_status=(200, 204))

    def vaciar_carrito(self, usuario_id: int) -> Any:
        """Elimina todos los productos del carrito del usuario."""
        payload = {"usuarioId": usuario_id}
        return self.request("DELETE", "/shopcart/", json=payload, expected_status=(200, 204))

    def sincronizar_carrito(self, usuario_id: int, items: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        """Reemplaza completamente el contenido del carrito del usuario."""
        payload = {"usuarioId": usuario_id, "items": list(items)}
        return self.put("/shopcart/", json=payload, expected_status=(200, 204))



def obtener_cliente_stock(**kwargs: Any)  -> StockClient:
    """Helper para instanciar el cliente de stock con la configuración del proyecto.
    
    NOTA: Ahora usa la API de Stock EXTERNA a través de Nginx.
    La configuración viene de STOCK_API_BASE_URL en settings (http://nginx/stock/).
    """
    # Usar la configuración de Stock API desde settings (apunta a http://nginx/stock/)
    base_por_defecto = getattr(settings, "STOCK_API_BASE_URL", "http://nginx/stock/")
    base_url = kwargs.pop("base_url", None) or getattr(settings, "STOCK_API_BASE_URL", base_por_defecto)
    
    # Extraer use_service_token de kwargs antes de pasarlos a StockClient
    use_service_token = kwargs.pop("use_service_token", True)
    
    # Si se solicita usar service token y no hay token_provider, configurarlo
    if use_service_token and "token_provider" not in kwargs and "token" not in kwargs:
        try:
            # Forzar refresh del token para asegurar que esté vigente
            from utils.keycloak import get_service_account_token
            fresh_token = get_service_account_token(force_refresh=True)
            kwargs["token"] = fresh_token
        except Exception as e:
            # Si falla obtener el service token, registrar y continuar sin él
            import logging
            logging.getLogger(__name__).warning(f"No se pudo obtener service token: {e}")
    
    return StockClient(base_url=base_url, **kwargs)


def obtener_cliente_stock_externo(**kwargs: Any) -> StockClient:
    """Helper para conectar con una API de Stock EXTERNA (otro microservicio).
    
    Esta función usa la configuración de STOCK_API_BASE_URL del settings,
    que apunta a través de Nginx para enrutar a servicios externos.
    
    Usá esta función cuando necesites conectar con APIs de Stock reales
    que NO estén en la misma aplicación Django.
    """
    base_por_defecto = getattr(settings, "base_url_api", "http://nginx/stock/")
    base_url = kwargs.pop("base_url", None) or getattr(settings, "STOCK_API_BASE_URL", base_por_defecto)
    
    # Extraer use_service_token de kwargs
    use_service_token = kwargs.pop("use_service_token", True)
    
    if use_service_token and "token_provider" not in kwargs and "token" not in kwargs:
        try:
            from utils.keycloak import get_service_account_token
            fresh_token = get_service_account_token(force_refresh=True)
            kwargs["token"] = fresh_token
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"No se pudo obtener service token para API externa: {e}")
    
    return StockClient(base_url=base_url, **kwargs)
