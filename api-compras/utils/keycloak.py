from __future__ import annotations

import logging
import threading
import time
from typing import Optional

import requests

from django.conf import settings


log = logging.getLogger("keycloak")


class KeycloakServiceError(Exception):
    """Errores relacionados con la obtención de tokens de servicio."""


class KeycloakServiceTokenManager:
    """Obtiene y cachea tokens ``client_credentials`` de Keycloak."""

    def __init__(
        self,
        *,
        token_url: str,
        client_id: str,
        client_secret: str,
        scope: Optional[str] = None,
        timeout: float = 6.0,
        leeway: int = 30,
    ) -> None:
        if not client_id or not client_secret:
            raise KeycloakServiceError(
                "Se requieren KEYCLOAK_SERVICE_CLIENT_ID y KEYCLOAK_SERVICE_CLIENT_SECRET para usar client_credentials."
            )
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.timeout = timeout
        self.leeway = leeway
        self._token: Optional[str] = None
        self._expires_at: float = 0
        self._lock = threading.Lock()

    def _is_valid(self) -> bool:
        return bool(self._token and time.time() < (self._expires_at - self.leeway))

    def _refresh(self) -> str:
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        if self.scope:
            data["scope"] = self.scope
        log.debug("Solicitando token client_credentials a Keycloak (%s)", self.token_url)
        try:
            resp = requests.post(
                self.token_url,
                data=data,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise KeycloakServiceError("No se pudo contactar a Keycloak para obtener un token.") from exc
        if resp.status_code != 200:
            try:
                detail = resp.json()
            except Exception:  # pragma: no cover - fallback defensivo
                detail = resp.text
            raise KeycloakServiceError(
                f"Keycloak devolvió HTTP {resp.status_code} al pedir un token: {detail}"
            )
        payload = resp.json()
        token = payload.get("access_token")
        if not token:
            raise KeycloakServiceError("Keycloak no devolvió access_token.")
        expires_in = payload.get("expires_in", 60)
        self._token = token
        self._expires_at = time.time() + expires_in
        return token

    def get_token(self, force_refresh: bool = False) -> str:
        with self._lock:
            if not force_refresh and self._is_valid():
                return self._token  # type: ignore[return-value]
            return self._refresh()


_default_manager: Optional[KeycloakServiceTokenManager] = None
_manager_lock = threading.Lock()


def get_default_service_token_manager() -> KeycloakServiceTokenManager:
    global _default_manager
    with _manager_lock:
        if _default_manager is None:
            token_url = getattr(
                settings,
                "KEYCLOAK_TOKEN_URL",
                f"{settings.KEYCLOAK_SERVER_URL.rstrip('/')}/protocol/openid-connect/token",
            )
            client_id = getattr(settings, "KEYCLOAK_SERVICE_CLIENT_ID", settings.KEYCLOAK_CLIENT_ID)
            client_secret = getattr(settings, "KEYCLOAK_SERVICE_CLIENT_SECRET", settings.KEYCLOAK_CLIENT_SECRET)
            scope = getattr(settings, "KEYCLOAK_SERVICE_SCOPE", None)
            if not client_secret:
                raise KeycloakServiceError(
                    "No se configuró KEYCLOAK_SERVICE_CLIENT_SECRET. Keycloak no permitirá client_credentials."
                )
            _default_manager = KeycloakServiceTokenManager(
                token_url=token_url,
                client_id=client_id,
                client_secret=client_secret,
                scope=scope,
            )
        return _default_manager


def get_service_account_token(force_refresh: bool = False) -> str:
    """Helper simple para obtener el JWT del cliente configurado."""
    manager = get_default_service_token_manager()
    return manager.get_token(force_refresh=force_refresh)


def get_service_token_provider(silent: bool = True):
    """Devuelve un callable que obtiene siempre el token válido.

    Si ``silent`` es ``True`` se devuelve ``None`` cuando la config no está
    completa. Caso contrario, se propaga la excepción.
    """
    try:
        manager = get_default_service_token_manager()
    except KeycloakServiceError:
        if silent:
            return None
        raise
    return manager.get_token
