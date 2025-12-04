from django.apps import AppConfig


class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.modulos.login'

    def ready(self):
        import apps.modulos.login.signals  # noqa: F401
        from apps.modulos.login.keycloak_oidc import KeycloakOpenIDConnectAdapter
        from allauth.socialaccount.providers.openid_connect import (
            provider as oidc_provider,
            views as oidc_views,
        )

        # Replace allauth's default adapter so discovery/token calls hit the
        # internal Keycloak hostname instead of localhost inside Docker.
        oidc_views.OpenIDConnectOAuth2Adapter = KeycloakOpenIDConnectAdapter
        oidc_provider.OpenIDConnectProvider.oauth2_adapter_class = (
            KeycloakOpenIDConnectAdapter
        )
