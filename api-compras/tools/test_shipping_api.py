"""
Script de smoke test para el endpoint de logistica.

Usa las mismas credenciales que tu .env (KEYCLOAK_SERVICE_CLIENT_ID /
KEYCLOAK_SERVICE_CLIENT_SECRET / KEYCLOAK_SERVICE_SCOPE). Por defecto
usa el client grupo-04 y scope `productos:read` que ya tienes en .env.
Luego envia un POST a `/shipping` en `shipping-back`.

Uso (dentro del contenedor django):
    docker-compose exec django python tools/test_shipping_api.py

Variables opcionales:
    KEYCLOAK_BASE_URL               (default: http://keycloak:8080)
    KEYCLOAK_REALM                  (default: ds-2025-realm)
    KEYCLOAK_SERVICE_CLIENT_ID      (default: grupo-04)
    KEYCLOAK_SERVICE_CLIENT_SECRET  (default: 6be1bec1-9472-499f-ab37-883d78f57829)
    KEYCLOAK_SERVICE_SCOPE          (default: productos:read)
    SHIPPING_API_URL                (default: http://shipping-back:3010/shipping)
"""

from __future__ import annotations

import json
import os
import sys
from typing import Dict, Tuple

import requests


def build_token_url() -> str:
    base = os.getenv("KEYCLOAK_BASE_URL", "http://keycloak:8080").rstrip("/")
    realm = os.getenv("KEYCLOAK_REALM", "ds-2025-realm")
    # Permite usar directamente KEYCLOAK_SERVER_URL si viene ya con /realms/<realm>
    server_url = os.getenv("KEYCLOAK_SERVER_URL")
    if server_url:
        return f"{server_url.rstrip('/')}/protocol/openid-connect/token"
    return f"{base}/realms/{realm}/protocol/openid-connect/token"


def get_service_token() -> str:
    client_id = os.getenv("KEYCLOAK_SERVICE_CLIENT_ID") or os.getenv("KEYCLOAK_CLIENT_ID") or "grupo-04"
    client_secret = os.getenv("KEYCLOAK_SERVICE_CLIENT_SECRET") or os.getenv("KEYCLOAK_CLIENT_SECRET") or "6be1bec1-9472-499f-ab37-883d78f57829"
    default_scope = "productos:read"
    scope = os.getenv("KEYCLOAK_SERVICE_SCOPE", default_scope)
    if not scope or not scope.strip():
        scope = default_scope

    if not client_id or not client_secret:
        raise RuntimeError("Faltan credenciales del cliente configurado en .env.")

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    if scope:
        data["scope"] = scope
    resp = requests.post(build_token_url(), data=data, timeout=8)
    if resp.status_code != 200:
        raise RuntimeError(f"Keycloak devolvio HTTP {resp.status_code}: {resp.text}")
    token = resp.json().get("access_token")
    if not token:
        raise RuntimeError(f"Keycloak no devolvio access_token: {resp.text}")
    return token


def call_shipping(token: str) -> Tuple[int, str]:
    shipping_url = os.getenv("SHIPPING_API_URL", "http://shipping-back:3010/shipping")
    payload: Dict[str, object] = {
        "order_id": 123,
        "user_id": 1,
        "delivery_address": {
            "street": "X",
            "city": "Y",
            "state": "BA",
            "postal_code": "A1234ABC",
            "country": "AR",
        },
        "transport_type": "road",
        "products": [{"id": 1, "quantity": 1}],
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    resp = requests.post(shipping_url, json=payload, headers=headers, timeout=12)
    body = resp.text
    try:
        body = json.dumps(resp.json(), ensure_ascii=False, indent=2)
    except Exception:
        body = body[:500]
    return resp.status_code, body


def main() -> int:
    try:
        token = get_service_token()
    except Exception as exc:  # noqa: BLE001
        print(f"[!] Error obteniendo token de servicio: {exc}")
        return 1

    try:
        status, body = call_shipping(token)
    except Exception as exc:  # noqa: BLE001
        print(f"[!] Error llamando al shipping: {exc}")
        return 1

    print(f"[+] Respuesta shipping-back: HTTP {status}")
    print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
