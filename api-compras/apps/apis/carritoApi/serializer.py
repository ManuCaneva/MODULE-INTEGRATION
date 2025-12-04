from rest_framework import serializers
from .models import Carrito, ItemCarrito


from utils.apiCliente.stock import StockClient
from django.conf import settings

class CartItemSerializer(serializers.ModelSerializer):
	productId = serializers.IntegerField(source='producto_id')
	quantity = serializers.IntegerField(source='cantidad')
	product = serializers.SerializerMethodField()

	class Meta:
		model = ItemCarrito
		fields = ['productId', 'quantity', 'product']

	def get_product(self, obj):
		# Primero intenta obtener el producto del contexto (batch)
		productos = self.context.get('productos', [])
		if productos:
			# Si productos es una lista, buscar por ID
			if isinstance(productos, list):
				for p in productos:
					if int(p.get('id')) == int(obj.producto_id):
						return p
			# Si productos es un dict indexado por ID
			elif isinstance(productos, dict) and obj.producto_id in productos:
				return productos[obj.producto_id]
		
		# Si USE_MOCK_APIS está activo, devolver datos mock
		use_mock = self.context.get('use_mock_apis', False)
		if use_mock:
			# Productos mock básicos
			precios_mock = {
				1: {"id": 1, "nombre": "Laptop Dell XPS 13", "precio": 1299.99},
				2: {"id": 2, "nombre": "iPhone 15 Pro", "precio": 999.00},
				3: {"id": 3, "nombre": "Samsung Galaxy S24", "precio": 849.00},
				4: {"id": 4, "nombre": "AirPods Pro", "precio": 249.00},
				5: {"id": 5, "nombre": "Zapatillas Nike Air", "precio": 89.99},
			}
			return precios_mock.get(obj.producto_id, {"id": obj.producto_id, "nombre": f"Producto {obj.producto_id}", "precio": 99.99})
		
		# Si no hay productos en contexto y no es mock, hace la petición individual
		try:
			stock_client = StockClient(base_url=settings.STOCK_API_BASE_URL)
			producto = stock_client.obtener_producto(obj.producto_id)
			return producto
		except Exception:
			return None


class CartSerializer(serializers.ModelSerializer):
	items = CartItemSerializer(many=True, read_only=True)
	total = serializers.SerializerMethodField()

	class Meta:
		model = Carrito
		fields = ['items', 'total']

	def get_total(self, obj):
		# Suma de cantidades, puedes ajustar para sumar precios si tienes acceso a los productos
		return sum(item.cantidad for item in obj.items.all())

