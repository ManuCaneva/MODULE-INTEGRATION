from django.urls import path
from . import views

urlpatterns = [
    # Ruta principal (menú de selección)
    path('', views.administracion_view, name='administracion'),

    # Rutas de los módulos específicos
    path('stock/', views.admin_stock_view, name='admin_stock'),
    path('logistica/', views.admin_logistica_view, name='admin_logistica'),
    path('compras/', views.admin_compras_view, name='admin_compras'),

    # --- Rutas placeholder para que no falle el dashboard ---
    path('items/nuevo/', views.administracion_view, name='admin_items_nuevo'),
    path('reportes/', views.administracion_view, name='admin_reportes'),
    path('configuracion/', views.administracion_view, name='admin_config'),
    path('transacciones/', views.administracion_view, name='admin_transacciones'),
]

