from django.urls import path
from . import views  # Es una buena práctica usar la importación relativa con "."

app_name = 'pedidos'

urlpatterns = [
    # path('QR/', views.AnalisisQR, name='AnalizarQR'),
    path('pago/fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago/exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('checkout/', views.checkout_view, name='checkout'),
        path('api/checkout/confirm/', views.api_checkout_confirm, name='api_checkout_confirm'),
    path('admin/', views.listar_pedidos, name='listar_pedidos_admin'),
    path('', views.mis_pedidos, name='mis_pedidos'),
]