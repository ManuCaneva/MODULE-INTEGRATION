from __future__ import annotations
from typing import Any, Dict, Optional

from django.conf import settings
from utils.apiCliente.base import BaseAPIClient
from utils.keycloak import get_service_token_provider

class StockClient(BaseAPIClient):
    """
    Cliente para consumir la API de Stock.
    Incluye autenticación automática para evitar el error 401.
    """

    def __init__(self, **kwargs):
        # 1. Configura la URL base si no viene dada
        if 'base_url' not in kwargs:
            kwargs['base_url'] = getattr(settings, "STOCK_API_BASE_URL", "http://gateway:80/stock")
        
        # 2. INYECTA EL TOKEN (Esto arregla el error 401)
        kwargs['token_provider'] = get_service_token_provider(silent=True)
        
        super().__init__(**kwargs)

    def listar_productos(self, page: int = 1, limit: int = 20, q: Optional[str] = None, categoriaId: Optional[int] = None):
        params = {"page": page, "limit": limit}
        if q: params["q"] = q
        if categoriaId: params["categoriaId"] = categoriaId
        return self.get("/productos", params=params, expected_status=200)

    def obtener_producto(self, productoId: int):
        return self.get(f"/productos/{productoId}", expected_status=200)

    def listar_categorias(self):
        return self.get("/categorias", expected_status=200)

    def obtener_categoria(self, categoriaId: int):
        return self.get(f"/categorias/{categoriaId}", expected_status=200)

    def reservar_stock(self, idCompra: str, usuarioId: int, productos: list):
        reserva_data = { "idCompra": idCompra, "usuarioId": usuarioId, "productos": productos }
        return self.post("/reservas", json=reserva_data, expected_status=(200, 201))

    def listar_reservas(self,  usuarioId: int, page: int = 1, limit: int = 20, estado: Optional[str] = None):
        params = {"usuarioId": usuarioId, "page": page, "limit": limit}
        if estado: params["estado"] = estado
        return self.get("/reservas", params=params, expected_status=200)

    def obtener_reserva(self, idReserva: int, usuarioId: int):
        params = {"usuarioId": usuarioId}
        return self.get(f"/reservas/{idReserva}", params=params, expected_status=200)
    
    def liberar_stock(self, idReserva: int, usuarioId: int, motivo: str):
        body = {"idReserva": idReserva, "usuarioId": usuarioId, "motivo": motivo}
        return self.post("/reservas/liberar", json=body, expected_status=(200, 201))