from django.urls import path

from apps.modulos.login.views import login_view, registro_view, cerrar_sesion

app_name = "login"

urlpatterns = [
    path('login/', login_view, name="login"),
    path('registro/', registro_view, name='registro'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),
]
