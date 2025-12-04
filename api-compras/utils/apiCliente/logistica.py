# utils/api_clients/logistica.py
from __future__ import annotations

from typing import Any, Dict, List, Optional
from .base import BaseAPIClient


class LogisticsClient(BaseAPIClient):
    def create_shipment(self, order_id: int, user_id: int, delivery_address: dict, transport_type: str, products: list) -> dict:
        """
        Crea un nuevo envío para una orden, según el contrato OpenAPI.
        order_id: ID de la orden
        user_id: ID del usuario
        delivery_address: dict con street, city, state, postal_code, country
        transport_type: método de transporte elegido (ej: 'air', 'road')
        products: lista de dicts {id, quantity}
        """
        body = {
            "order_id": order_id,
            "user_id": user_id,
            "delivery_address": delivery_address,
            "transport_type": transport_type,
            "products": products
        }
        return self.post("/shipping", json=body, expected_status=(200, 201))
    """
    Cliente para el servicio de Transporte / Logística.

    Métodos implementados (mapean a los endpoints OpenAPI):
    - calculate_shipping_cost -> POST /shipping/cost
    - get_transport_methods -> GET /shipping/transport-methods
    - list_shipments -> GET /shipping
    - get_shipment -> GET /shipping/{shipping_id}
    - cancel_shipment -> POST /shipping/{shipping_id}/cancel
    """

    def calculate_shipping_cost(self, delivery_address: Dict[str, Any], products: List[Dict[str, Any]], transport_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Calcula un presupuesto de envío (no persiste nada).

        delivery_address: dict con keys street, city, state, postal_code, country
        products: lista de {id, quantity}
        transport_type: opcional, p.ej. 'air', 'road'
        """
        body: Dict[str, Any] = {"delivery_address": delivery_address, "products": products}
        if transport_type:
            body["transport_type"] = transport_type
        return self.post("/shipping/cost", json=body, expected_status=200)

    def get_transport_methods(self) -> Dict[str, Any]:
        """Devuelve los métodos de transporte disponibles (air, road, rail, sea)."""
        return self.get("/shipping/transport-methods", expected_status=200)

    def list_shipments(self, user_id: Optional[int] = None, status: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """
        Lista envíos con filtros opcionales. Devuelve estructura paginada.
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if user_id is not None:
            params["user_id"] = user_id
        if status:
            params["status"] = status
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        return self.get("/shipping", params=params, expected_status=200)

    def get_shipment(self, shipping_id: int) -> Dict[str, Any]:
        """Obtiene detalle completo de un envío por su id."""
        return self.get(f"/shipping/{shipping_id}", expected_status=200)

    def cancel_shipment(self, shipping_id: int) -> Dict[str, Any]:
        """
        Cancela un envío. El servicio puede responder 200 (ok) o 4xx según la lógica.
        """
        return self.post(f"/shipping/{shipping_id}/cancel", json={}, expected_status=200)

    # --------------------------------------------------------------
    # Endpoints de Tracking (alias explícitos según OpenAPI externa)
    # --------------------------------------------------------------
    def create_tracking(
        self,
        *,
        order_id: int,
        user_id: int,
        delivery_address: Dict[str, Any],
        transport_type: str,
        products: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Crea un tracking en Logística (POST /logistics/tracking).

        Esta es una envoltura semántica del endpoint de tracking indicado
        por la OpenAPI compartida entre Compras ↔ Logística. Si el
        servicio usa "/shipping" de forma equivalente, mantenemos ambos
        métodos por compatibilidad.
        """
        payload: Dict[str, Any] = {
            "order_id": order_id,
            "user_id": user_id,
            "delivery_address": delivery_address,
            "transport_type": transport_type,
            "products": products,
        }
        # Ruta según OpenAPI de logística expuesta a compras
        return self.post("/logistics/tracking", json=payload, expected_status=(200, 201))

    def get_tracking(self, tracking_id: int) -> Dict[str, Any]:
        """Obtiene el estado de un tracking (GET /logistics/tracking/{id})."""
        return self.get(f"/logistics/tracking/{tracking_id}", expected_status=200)
