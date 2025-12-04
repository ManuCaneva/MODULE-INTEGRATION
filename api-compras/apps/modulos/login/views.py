import logging
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from allauth.socialaccount.adapter import get_adapter


log = logging.getLogger("app")


def _build_keycloak_login_url(request, next_url=None):
    """Construye la URL de login hacia Keycloak utilizando allauth."""
    redirect_url = None
    if next_url:
        redirect_url = request.build_absolute_uri(next_url)

    try:
        provider = get_adapter().get_provider(request, 'keycloak')
        return provider.get_login_url(
            request,
            process='login',
            redirect_url=redirect_url,
        )
    except Exception:  # pragma: no cover - fallback defensivo
        log.exception("No se pudo generar la URL de login de Keycloak desde allauth.")
        params = {
            'client_id': settings.KEYCLOAK_CLIENT_ID,
            'response_type': 'code',
            'scope': ' '.join(settings.KEYCLOAK_SCOPE),
            'redirect_uri': settings.KEYCLOAK_LOGIN_REDIRECT_URI,
        }
        if redirect_url:
            params['state'] = redirect_url
        base_url = (
            f"{settings.KEYCLOAK_PUBLIC_SERVER_URL.rstrip('/')}/"
            "protocol/openid-connect/auth"
        )
        return f"{base_url}?{urlencode(params)}"


def _build_keycloak_registration_url(request, next_url=None):
    """Devuelve la URL de registro de Keycloak con la redirección correcta."""
    redirect_url = None
    if next_url:
        redirect_url = request.build_absolute_uri(next_url)

    try:
        provider = get_adapter().get_provider(request, 'keycloak')
        return provider.get_login_url(
            request,
            auth_params={'kc_action': 'register'},
            redirect_url=redirect_url,
        )
    except Exception:  # pragma: no cover - fallback defensivo
        log.exception("No se pudo generar la URL de registro de Keycloak desde allauth.")
        params = {
            'client_id': settings.KEYCLOAK_CLIENT_ID,
            'response_type': 'code',
            'scope': ' '.join(settings.KEYCLOAK_SCOPE),
            'redirect_uri': settings.KEYCLOAK_LOGIN_REDIRECT_URI,
            'kc_action': 'register',
        }
        if redirect_url:
            params['state'] = redirect_url
        base_url = (
            f"{settings.KEYCLOAK_PUBLIC_SERVER_URL.rstrip('/')}/"
            "protocol/openid-connect/auth"
        )
        return f"{base_url}?{urlencode(params)}"


def _get_safe_next_url(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    if not next_url:
        return None
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return next_url
    log.warning("Parametro next=%s descartado por no ser seguro", next_url)
    return None


def login_view(request):
    next_url = _get_safe_next_url(request) or settings.LOGIN_REDIRECT_URL
    keycloak_login_url = _build_keycloak_login_url(request, next_url)
    keycloak_registration_url = _build_keycloak_registration_url(request, next_url)

    if request.method == "POST":
        log.info("Redirigiendo login hacia Keycloak desde POST.")
        return redirect(keycloak_login_url)

    auto_redirect = request.GET.get("manual") != "1"
    if auto_redirect:
        log.info("Auto redirigiendo login hacia Keycloak desde GET.")

    context = {
        'active_tab': 'login',
        'keycloak_login_url': keycloak_login_url,
        'keycloak_registration_url': keycloak_registration_url,
        'auto_redirect': auto_redirect,
    }
    return render(request, "login_registro.html", context)


def registro_view(request):
    next_url = _get_safe_next_url(request) or settings.LOGIN_REDIRECT_URL
    keycloak_registration_url = _build_keycloak_registration_url(request, next_url)
    log.info("Redirigiendo registro hacia Keycloak.")
    return redirect(keycloak_registration_url)


def cerrar_sesion(request):
    logout(request)
    base_logout_url = (
        f"{settings.KEYCLOAK_PUBLIC_SERVER_URL.rstrip('/')}/"
        "protocol/openid-connect/logout"
    )
    params = {
        'client_id': settings.KEYCLOAK_CLIENT_ID,
    }
    if settings.KEYCLOAK_LOGOUT_REDIRECT_URI:
        params['post_logout_redirect_uri'] = settings.KEYCLOAK_LOGOUT_REDIRECT_URI
    logout_url = f"{base_logout_url}?{urlencode(params)}"
    return redirect(logout_url)
