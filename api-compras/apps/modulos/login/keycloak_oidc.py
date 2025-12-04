"""Custom OpenID Connect adapter that routes server-to-server calls to Keycloak's
internal hostname while keeping public endpoints intact for browser redirects."""

from __future__ import annotations

from copy import deepcopy
from urllib.parse import urlparse, urlunparse

from django.conf import settings

from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.openid_connect.views import (
    OpenIDConnectOAuth2Adapter,
)


class KeycloakOpenIDConnectAdapter(OpenIDConnectOAuth2Adapter):
    """Overrides default adapter to allow split public/internal Keycloak hosts."""

    _INTERNAL_ENDPOINT_KEYS = (
        "token_endpoint",
        "userinfo_endpoint",
        "introspection_endpoint",
        "revocation_endpoint",
    )
    _PUBLIC_ENDPOINT_KEYS = (
        "authorization_endpoint",
        "end_session_endpoint",
    )

    def _should_rewrite(self) -> bool:
        internal = getattr(settings, "KEYCLOAK_BASE_URL", "").strip()
        public = getattr(settings, "KEYCLOAK_PUBLIC_BASE_URL", "").strip() or internal
        return bool(internal and public and internal.rstrip("/") != public.rstrip("/"))

    def _rebase_url(self, url: str | None) -> str | None:
        if not url or not self._should_rewrite():
            return url
        internal_base = getattr(settings, "KEYCLOAK_BASE_URL").strip().rstrip("/")
        parsed_internal = urlparse(internal_base)
        if not parsed_internal.scheme or not parsed_internal.netloc:
            return url
        parsed = urlparse(url)
        rebased = parsed._replace(
            scheme=parsed_internal.scheme,
            netloc=parsed_internal.netloc,
        )
        return urlunparse(rebased)

    def _rebase_to_public(self, url: str | None) -> str | None:
        if not url or not self._should_rewrite():
            return url
        public_base = getattr(settings, "KEYCLOAK_PUBLIC_BASE_URL", "").strip().rstrip("/")
        parsed_public = urlparse(public_base)
        if not parsed_public.scheme or not parsed_public.netloc:
            return url
        parsed = urlparse(url)
        rebased = parsed._replace(
            scheme=parsed_public.scheme,
            netloc=parsed_public.netloc,
        )
        return urlunparse(rebased)

    def _get_internal_server_url(self) -> str:
        server_url = self.get_provider().server_url
        return self._rebase_url(server_url) or server_url

    @property
    def openid_config(self):
        if hasattr(self, "_patched_openid_config"):
            return self._patched_openid_config

        server_url = self._get_internal_server_url()
        resp = get_adapter().get_requests_session().get(server_url)
        resp.raise_for_status()
        config = resp.json()

        if self._should_rewrite():
            patched = deepcopy(config)
            for key in self._INTERNAL_ENDPOINT_KEYS:
                patched[key] = self._rebase_url(patched.get(key))
            for key in self._PUBLIC_ENDPOINT_KEYS:
                patched[key] = self._rebase_to_public(patched.get(key))
            self._patched_openid_config = patched
        else:
            self._patched_openid_config = config
        return self._patched_openid_config

