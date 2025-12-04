from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Categoria
from .serializer import CategoriaSerializer
from rest_framework import status
from utils.apiCliente.stock import StockClient
from utils.keycloak import get_service_token_provider
from django.conf import settings
import math
from apps.apis.productoApi.hardcode import MOCK_PRODUCTS

# ============================
# Productos MOCK para modo demo
# ============================



class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar categorías
    Proporciona automáticamente: list, create, retrieve, update, destroy
    """
    queryset = Categoria.objects.filter(activo=True)
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        """Filtra solo categorías activas"""
        return Categoria.objects.filter(activo=True).order_by('nombre')


class ProductoViewSet(viewsets.ViewSet):
    """
    ViewSet para gestionar productos desde la API externa de Stock
    o desde un mock local según configuración.
    """

    def list(self, request):
        """GET /productos/ - Listar productos"""
        use_mock = getattr(settings, "USE_MOCK_APIS", True)

        if use_mock:
            # ==========================
            # MODO MOCK: lista local + paginación simulada
            # ==========================
            productos = MOCK_PRODUCTS.copy()

            # filtros básicos por query params
            search = request.query_params.get("search") or request.query_params.get("q") or ""
            categoria = request.query_params.get("categoria") or ""
            marca = request.query_params.get("marca") or ""

            search = search.strip().lower()
            categoria = categoria.strip()
            marca = marca.strip()

            def _filtrar(p):
                if search:
                    nombre = (p.get("nombre") or "").lower()
                    desc = (p.get("descripcion") or "").lower()
                    if search not in nombre and search not in desc:
                        return False
                if categoria and p.get("categoria") != categoria:
                    return False
                if marca and p.get("marca") != marca:
                    return False
                return True

            productos_filtrados = [p for p in productos if _filtrar(p)]

            # paginación
            try:
                page = int(request.query_params.get("page", 1))
            except ValueError:
                page = 1
            try:
                limit = int(request.query_params.get("limit", 12))
            except ValueError:
                limit = 12

            if page < 1:
                page = 1
            if limit < 1:
                limit = 12

            total = len(productos_filtrados)
            total_pages = math.ceil(total / limit) if limit else 1

            start = (page - 1) * limit
            end = start + limit
            data = productos_filtrados[start:end]

            response_payload = {
                "data": data,
                "pagination": {
                    "page": page,
                    "per_page": limit,
                    "total": total,
                    "total_pages": total_pages,
                },
            }
            return Response(response_payload, status=status.HTTP_200_OK)

        # ==========================
        # MODO REAL: llamar al servicio de Stock
        # ==========================
        stock_client = StockClient(base_url=settings.STOCK_API_BASE_URL)
        try:
            categoria = request.query_params.get('categoria')
            search = request.query_params.get('search')
            page = request.query_params.get('page', 1)
            limit = request.query_params.get('limit', 20)

            productos = stock_client.listar_productos(
                page=int(page),
                limit=int(limit),
                q=search,
                categoriaId=int(categoria) if categoria else None
            )
            return Response(productos, status=status.HTTP_200_OK)
        except Exception as e:
            if 'Connection' in str(e):
                return Response({
                    "error": "Servicio Stock no disponible",
                    "code": "STOCK_SERVICE_UNAVAILABLE"
                }, status=status.HTTP_502_BAD_GATEWAY)
            return Response({
                "error": "Error interno del servidor",
                "code": "INTERNAL_ERROR"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """GET /productos/{id}/ - Detalle de producto"""
        use_mock = getattr(settings, "USE_MOCK_APIS", True)

        if use_mock:
            try:
                pid = int(pk)
            except (TypeError, ValueError):
                return Response({
                    "error": "ID de producto inválido",
                    "code": "INVALID_PRODUCT_ID"
                }, status=status.HTTP_400_BAD_REQUEST)

            for p in MOCK_PRODUCTS:
                if p.get("id") == pid:
                    return Response(p, status=status.HTTP_200_OK)

            return Response({
                "error": "Producto no encontrado",
                "code": "PRODUCT_NOT_FOUND"
            }, status=status.HTTP_404_NOT_FOUND)

        # MODO REAL
        stock_client = StockClient(base_url=settings.STOCK_API_BASE_URL)
        try:
            producto = stock_client.obtener_producto(int(pk))
            if not producto:
                return Response({
                    "error": "Producto no encontrado",
                    "code": "PRODUCT_NOT_FOUND"
                }, status=status.HTTP_404_NOT_FOUND)
            return Response(producto, status=status.HTTP_200_OK)
        except Exception as e:
            if 'Connection' in str(e):
                return Response({
                    "error": "Servicio Stock no disponible",
                    "code": "STOCK_SERVICE_UNAVAILABLE"
                }, status=status.HTTP_502_BAD_GATEWAY)
            return Response({
                "error": "Error interno del servidor",
                "code": "INTERNAL_ERROR"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
