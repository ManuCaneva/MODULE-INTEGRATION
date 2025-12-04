"""URLs del frontend según especificación OpenAPI.

Estas rutas mapean los endpoints públicos del frontend a las acciones
correspondientes del PedidoViewSet, manteniendo compatibilidad con el
contrato OpenAPI definido para el cliente.
"""
from django.urls import path
from .views import PedidoViewSet

# Instancias de las acciones del ViewSet
history_list = PedidoViewSet.as_view({'get': 'history'})
history_detail = PedidoViewSet.as_view({'get': 'history_detail'})
cancelar = PedidoViewSet.as_view({'delete': 'cancelar'})
checkout = PedidoViewSet.as_view({'post': 'crear_desde_carrito'})

urlpatterns = [
    # GET /api/shopcart/history - Ver historial de pedidos
    path('shopcart/history', history_list, name='shopcart-history'),
    
    # GET /api/shopcart/history/{id} - Ver pedido específico
    # DELETE /api/shopcart/history/{id} - Cancelar pedido (mismo endpoint)
    path('shopcart/history/<int:pk>', PedidoViewSet.as_view({
        'get': 'history_detail',
        'delete': 'cancelar'
    }), name='shopcart-history-detail'),
    
    # POST /api/shopcart/checkout - Confirmar pedido desde carrito
    path('shopcart/checkout', checkout, name='shopcart-checkout'),
]

