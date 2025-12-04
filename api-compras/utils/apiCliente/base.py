# utils/api_clients/base.py
from __future__ import annotations

from typing import Any, Dict, Optional, Callable
import requests

# Excepción personalizada para errores de API
class APIError(Exception):
    def __init__(self, message: str, *, status: int | None = None,
                 url: str | None = None, payload: Any = None):
        super().__init__(message)
        self.status = status
        self.url = url
        self.payload = payload

# Cliente base para consumir APIs RESTful
class BaseAPIClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = 8.0,
        max_retries: int = 2,
        default_headers: Optional[Dict[str, str]] = None,
        token: str | None = None,
        api_key: str | None = None,
        token_provider: Optional[Callable[[], str]] = None,
    ):
        if not base_url:
            raise ValueError("base_url es requerido")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self._token_provider = token_provider

        self.default_headers: Dict[str, str] = {"Accept": "application/json"}
        if default_headers:
            self.default_headers.update(default_headers)
        if token:
            self.default_headers["Authorization"] = f"Bearer {token}"
        if api_key:
            self.default_headers.setdefault("X-API-Key", api_key)

    def _url(self, path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path
        return self.base_url + path

    def _obtain_authorization_header(self) -> str | None:
        if not self._token_provider:
            return None
        try:
            token = self._token_provider()
        except Exception as exc:  # pragma: no cover - infraestructura externa
            raise APIError("No se pudo obtener un token dinámico para la llamada HTTP.") from exc
        if token:
            if token.lower().startswith("bearer "):
                return token
            return f"Bearer {token}"
        return None

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Dict[str, Any] | None = None,
        json: Any = None,
        expected_status: int | tuple[int, ...] | None = 200,
        headers: Dict[str, str] | None = None,
    ) -> Any:
        url = self._url(path)
        _headers = dict(self.default_headers)
        if headers:
            _headers.update(headers)
        if "Authorization" not in _headers:
            auth_header = self._obtain_authorization_header()
            if auth_header:
                _headers["Authorization"] = auth_header

        last_exc: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = self.session.request(
                    method.upper(),
                    url,
                    params=params,
                    json=json,
                    headers=_headers,
                    timeout=self.timeout,
                )
                # validar status esperado(s)
                if expected_status is not None:
                    oks = expected_status if isinstance(expected_status, tuple) else (expected_status,)
                    if resp.status_code not in oks:
                        try:
                            payload = resp.json()
                        except Exception:
                            payload = resp.text
                        raise APIError(
                            f"HTTP {resp.status_code} calling {url}",
                            status=resp.status_code, url=url, payload=payload
                        )
                # devolver JSON si hay
                if resp.headers.get("Content-Type", "").startswith("application/json"):
                    return resp.json()
                return resp.text
            except (requests.Timeout, requests.ConnectionError) as exc:
                last_exc = exc
                if attempt >= self.max_retries:
                    raise APIError(f"Timeout/Conexión a {url} falló tras reintentos") from exc
        raise last_exc  # no debería llegar
    
    # helpers cómodos
    def get(self, path: str, *, params=None, expected_status=200, headers=None):
        return self.request("GET", path, params=params, expected_status=expected_status, headers=headers)

    def post(self, path: str, *, json=None, expected_status=201, headers=None):
        return self.request("POST", path, json=json, expected_status=expected_status, headers=headers)

    def put(self, path: str, *, json=None, expected_status=200, headers=None):
        return self.request("PUT", path, json=json, expected_status=expected_status, headers=headers)

    def delete(self, path: str, *, expected_status=204, headers=None):
        return self.request("DELETE", path, expected_status=expected_status, headers=headers)


