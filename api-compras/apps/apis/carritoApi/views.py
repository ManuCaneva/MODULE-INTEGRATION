from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from .models import Carrito, ItemCarrito
import logging
logger = logging.getLogger(__name__)
from .serializer import CartSerializer
from .client import obtener_cliente_stock_externo
from utils.apiCliente import APIError


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """GET /api/shopcart/ - Ver carrito"""
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        logger.info("Carrito:list user=%s items=%s", request.user.id, carrito.items.count())
        
        # Verificar si usamos APIs externas o modo mock/desarrollo
        use_external_apis = not getattr(settings, 'USE_MOCK_APIS', True)
        use_mock_apis = not use_external_apis
        productos = []
        
        if use_external_apis:
            # Modo PRODUCCIÓN: Obtener datos reales de la API de Stock
            items = carrito.items.all()
            product_ids = [item.producto_id for item in items]
            stock_client = obtener_cliente_stock_externo()
            
            for id in product_ids:
                try:
                    producto = stock_client.obtener_producto(id)
                except APIError as exc:
                    logger.error("Carrito:list fallo stock id=%s error=%s", id, exc)
                    return Response(
                        {"error": "Error al obtener productos del carrito", "code": "PRODUCT_FETCH_ERROR"},
                        status=status.HTTP_502_BAD_GATEWAY,
                    )
                if not producto:
                    return Response(
                        {"error": "Producto no encontrado en stock", "code": "PRODUCT_NOT_FOUND"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                productos.append(producto)
        
        # Pasar flag de mock al serializer para que use datos mock si es necesario
        serializer = CartSerializer(carrito, context={'productos': productos, 'use_mock_apis': use_mock_apis})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """POST /api/shopcart/ - Agregar al carrito"""
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

        product_id = request.data.get('productId')
        quantity = request.data.get('quantity', 1)
        if not product_id or int(quantity) < 1:
            return Response({"error": "Datos inválidos", "code": "INVALID_DATA"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar si usamos APIs externas o modo mock/desarrollo
        use_external_apis = not getattr(settings, 'USE_MOCK_APIS', True)
        
        if use_external_apis:
            # Modo PRODUCCIÓN: Verificar con la API de Stock real
            stock_client = obtener_cliente_stock_externo()
            try:
                producto = stock_client.obtener_producto(product_id)
            except APIError as exc:
                logger.error("Carrito:create fallo stock product=%s error=%s", product_id, exc)
                return Response(
                    {"error": "Error consultando stock", "code": "PRODUCT_FETCH_ERROR"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )
            if not producto:
                return Response(
                    {"error": "Producto no encontrado", "code": "PRODUCT_NOT_FOUND"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Modo DESARROLLO/MOCK: Confiar en que el productId es válido
            # No verificamos con Stock porque es una API externa no disponible
            pass
        
        item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto_id=product_id)
        if not created:
            item.cantidad += int(quantity)
        else:
            item.cantidad = int(quantity)
        item.save()
        logger.info("Carrito:create user=%s product=%s qty=%s created=%s", request.user.id, product_id, quantity, created)
        return Response({"message": "Producto agregado al carrito"}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """PUT /api/shopcart/{productId}/ - Actualizar cantidad"""
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        quantity = request.data.get('quantity')
        if pk is None or quantity is None or int(quantity) < 1:
            return Response({"error": "Cantidad inválida", "code": "INVALID_QUANTITY"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            item = ItemCarrito.objects.get(carrito=carrito, producto_id=pk)
            item.cantidad = int(quantity)
            item.save()
            logger.info("Carrito:update user=%s product=%s qty=%s", request.user.id, pk, quantity)
            return Response({"message": "Carrito actualizado"}, status=status.HTTP_200_OK)
        except ItemCarrito.DoesNotExist:
            return Response({"error": "Producto no encontrado en el carrito", "code": "CART_ITEM_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """DELETE /api/shopcart/{productId}/ - Remover producto del carrito"""
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        if pk:
            try:
                item = ItemCarrito.objects.get(carrito=carrito, producto_id=pk)
                item.delete()
                logger.info("Carrito:delete item user=%s product=%s", request.user.id, pk)
                return Response({"message": "Producto removido del carrito"}, status=status.HTTP_200_OK)
            except ItemCarrito.DoesNotExist:
                return Response({"error": "Producto no encontrado en el carrito", "code": "CART_ITEM_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Debe especificar un producto para eliminar", "code": "MISSING_PRODUCT_ID"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'], url_path='clear')
    def clear(self, request):
        """DELETE /api/shopcart/clear/ - Vaciar todo el carrito"""
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        carrito.items.all().delete()
        logger.info("Carrito:clear user=%s", request.user.id)
        return Response({"message": "Carrito vaciado"}, status=status.HTTP_200_OK)
        
        
