# utils/api_clients.py
from __future__ import annotations
from typing import Any, Dict, Optional
from .base import BaseAPIClient


class StockClient(BaseAPIClient):
    """
    Cliente para consumir la API de Stock segÃºn el contrato OpenAPI.
    """

    def listar_productos(self, page: int = 1, limit: int = 20, q: Optional[str] = None, categoriaId: Optional[int] = None):
        params = {"page": page, "limit": limit}
        if q:
            params["q"] = q
        if categoriaId:
            params["categoriaId"] = categoriaId
        return self.get("/api/productos/", params=params, expected_status=200)
    def obtener_producto(self, productoId: int):
        return self.get(f"/api/productos/{productoId}/", expected_status=200)

    def reservar_stock(self, idCompra: str, usuarioId: int, productos: list):
        """
        Reserva stock segÃºn el schema ReservaInput.
        idCompra: identificador Ãºnico de la compra (str)
        usuarioId: ID del usuario que realiza la reserva (int)
        productos: lista de dicts con idProducto y cantidad
        """
        reserva_data = {
            "idCompra": idCompra,
            "usuarioId": usuarioId,
            "productos": productos
        }
        return self.post("/api/v1/reservas", json=reserva_data, expected_status=(200, 201))

    def listar_reservas(self,  usuarioId: int, page: int = 1, limit: int = 20, estado: Optional[str] = None):
        params = {"usuarioId": usuarioId, "page": page, "limit": limit}
        if estado:
            params["estado"] = estado
        return self.get("/api/v1/reservas", params=params, expected_status=200)

    def obtener_reserva(self, idReserva: int, usuarioId: int):
        params = {"usuarioId": usuarioId}
        return self.get(f"/api/v1/reservas/{idReserva}", params=params, expected_status=200)

    def listar_categorias(self):
        return self.get("/api/v1/categorias", expected_status=200)

    def obtener_categoria(self, categoriaId: int):
        return self.get(f"/api/v1/categorias/{categoriaId}", expected_status=200)
    
    # No sabemos si van o no
    def liberar_stock(self, idReserva: int, usuarioId: int, motivo: str):
        body = {"idReserva": idReserva, "usuarioId": usuarioId, "motivo": motivo}
        return self.post("/api/v1/liberar", json=body, expected_status=(200, 201))
    
