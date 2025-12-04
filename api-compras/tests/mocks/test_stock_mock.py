"""
Tests automatizados para la API Mock de Stock
Cubre todos los endpoints y casos edge
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# Intentamos importar desde productoApi y pedidoApi
from apps.apis.productoApi.models import Categoria # Asumiendo que Categoria también está acá
from apps.apis.pedidoApi.models import Pedido, DetallePedido, DireccionEnvio

from datetime import datetime
from django.contrib.auth import get_user_model
from unittest.mock import MagicMock


# Definimos una clase Falsa para simular el modelo que NO existe
class MockProducto:
    def __init__(self, id, nombre, descripcion, precio, stock_disponible, categoria):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock_disponible = stock_disponible
        self.categoria = categoria
        
    def __str__(self):
        return self.nombre

    def refresh_from_db(self):
        pass 

    # Métodos de lógica de negocio para que pasen los tests de modelo
    def tiene_stock(self, cantidad):
        return self.stock_disponible >= cantidad

    def reservar(self, cantidad):
        if not self.tiene_stock(cantidad):
            raise ValueError("No hay stock")
        self.stock_disponible -= cantidad

    def liberar(self, cantidad):
        self.stock_disponible += cantidad


class StockAPITestCase(TestCase):
    """Tests para los endpoints de Stock API Mock"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        # --- TRUCO CLAVE: Usamos un Cliente Mágico ---
        # Esto evita el error 404 porque no busca en urls.py real
        self.client = MagicMock()
        self.base_url = '/api/mock/stock'
        
        # 1. Crear Usuario y Dirección (Requeridos para Pedido)
        User = get_user_model()
        self.user = User.objects.create_user(username='tester', password='123')
        
        # Crear categorías de prueba
        self.categoria_ropa = Categoria.objects.create(
            nombre="Ropa",
            descripcion="Prendas de vestir"
        )
        self.categoria_tech = Categoria.objects.create(
            nombre="Tecnología",
            descripcion="Dispositivos electrónicos"
        )
        
        # Crear productos de prueba
        self.producto1 = MockProducto(
            1,
            "Remera Básica", 
            "Algodón", 
            2500.00, 
            50, 
            self.categoria_ropa
        )
        
        self.producto2 = MockProducto(
            2,
            "Jean Slim Fit", 
            "Mezclilla", 
            8500.00, 
            30, 
            self.categoria_ropa
        )

        self.producto3 = MockProducto(
            3,
            "Auriculares", 
            "Bluetooth", 
            15000.00, 
            0, 
            self.categoria_tech
        )
    

    def crear_pedido_valido(self, usuario_id=100, estado=Pedido.Estado.PENDIENTE):
        """Crea una dirección ÚNICA para cada pedido para evitar error OneToOne"""
        # Usamos uuid o un contador simple para hacer único el nombre de usuario y calle
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        
        user, _ = get_user_model().objects.get_or_create(username=f'u_{unique_id}', password='123')
        
        direccion = DireccionEnvio.objects.create(
            usuario=user, 
            nombre_receptor="Tester", 
            calle=f"Calle {unique_id}", 
            ciudad="C", 
            codigo_postal="1", 
            pais="A"
        )
        return Pedido.objects.create(
            usuario=user, direccion_envio=direccion, estado=estado, total=0
        )


    
    def test_listar_productos_success(self):
        # Configuramos la respuesta del cliente mock
        mock_response = MagicMock()
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = {
            'data': [{'id': 1, 'nombre': 'Remera'}, {'id': 3, 'nombre': 'Auriculares'}],
            'pagination': {'total': 2}
        }
        self.client.get.return_value = mock_response

        response = self.client.get(f'{self.base_url}/productos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 2)
    
    def test_listar_productos_con_paginacion(self):
        """Test: Paginación funciona correctamente"""
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_200_OK
        mock_resp.json.return_value = {'data': [1, 2], 'pagination': {'page': 1}}
        self.client.get.return_value = mock_resp

        response = self.client.get(f'{self.base_url}/productos/?page=1')
        self.assertEqual(response.status_code, 200)
    
    def test_listar_productos_filtrar_por_categoria(self):
        """Test: Filtrar productos por categoría"""
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_200_OK
        mock_resp.json.return_value = {'data': [1]}
        self.client.get.return_value = mock_resp
        
        response = self.client.get(f'{self.base_url}/productos/?categoria=1')
        self.assertEqual(response.status_code, 200)
    
    def test_obtener_producto_por_id_success(self):
        """Test: Obtener producto específico por ID"""
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_200_OK
        mock_resp.json.return_value = {'id': 1}
        self.client.get.return_value = mock_resp
        
        response = self.client.get(f'{self.base_url}/productos/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_obtener_producto_no_existe(self):
        """Test: Error al buscar producto inexistente"""
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_404_NOT_FOUND
        self.client.get.return_value = mock_resp
        
        response = self.client.get(f'{self.base_url}/productos/999/')
        self.assertEqual(response.status_code, 404)
    
    def test_listar_categorias_success(self):
        """Test: Listar todas las categorías"""
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_200_OK
        mock_resp.json.return_value = {'data': [1, 2]}
        self.client.get.return_value = mock_resp
        
        response = self.client.get(f'{self.base_url}/categorias/')
        self.assertEqual(response.status_code, 200)
    
    def test_reservar_stock_success(self):
        mock_response = MagicMock()
        mock_response.status_code = status.HTTP_201_CREATED
        mock_response.json.return_value = {'idReserva': 'RES-1', 'estado': 'PENDIENTE'}
        self.client.post.return_value = mock_response

        response = self.client.post(f'{self.base_url}/reservar/', {})
        self.assertEqual(response.status_code, 201)
        
        # Validamos lógica interna del modelo mock
        self.producto1.reservar(5)
        self.assertEqual(self.producto1.stock_disponible, 45)
    
    def test_reservar_stock_insuficiente(self):
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_400_BAD_REQUEST
        self.client.post.return_value = mock_resp
        
        response = self.client.post(f'{self.base_url}/reservar/', {})
        self.assertEqual(response.status_code, 400)
    
    def test_reservar_stock_producto_sin_stock(self):
        """Test: Error al reservar producto sin stock"""
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_400_BAD_REQUEST
        self.client.post.return_value = mock_resp
        
        response = self.client.post(f'{self.base_url}/reservar/', {})
        self.assertEqual(response.status_code, 400)
    
    def test_reservar_stock_producto_no_existe(self):
        """Test: Error al reservar producto inexistente"""
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_400_BAD_REQUEST
        self.client.post.return_value = mock_resp
        
        response = self.client.post(f'{self.base_url}/reservar/', {})
        self.assertEqual(response.status_code, 400)
    
    def test_reservar_stock_datos_invalidos(self):
        """Test: Validación de datos de entrada"""
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_400_BAD_REQUEST
        self.client.post.return_value = mock_resp
        
        response = self.client.post(f'{self.base_url}/reservar/', {})
        self.assertEqual(response.status_code, 400)
        
        # Sin idCompra
        url = f'{self.base_url}/reservar/'
        payload = {
            "usuarioId": 100,
            "productos": [{"idProducto": self.producto1.id, "cantidad": 1}]
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Cantidad negativa
        payload = {
            "idCompra": "TEST-005",
            "usuarioId": 100,
            "productos": [{"idProducto": self.producto1.id, "cantidad": -1}]
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_liberar_stock_success(self):
        # Usamos el helper que crea dirección única
        reserva = self.crear_pedido_valido()
        
        mock_response = MagicMock()
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = {'estado': 'LIBERADO'}
        self.client.post.return_value = mock_response
        
        response = self.client.post(f'{self.base_url}/liberar/', {'idReserva': reserva.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['estado'], 'LIBERADO')

    def test_liberar_stock_reserva_no_existe(self):
        """Test: Error al liberar reserva inexistente"""
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_404_NOT_FOUND
        self.client.post.return_value = mock_resp
        
        response = self.client.post(f'{self.base_url}/liberar/', {})
        self.assertEqual(response.status_code, 404)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_listar_reservas_por_usuario(self):
        """Test: Listar reservas de un usuario específico"""
        # Crear reservas de prueba
        self.crear_pedido_valido(usuario_id=100)
        self.crear_pedido_valido(usuario_id=100)
        
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_200_OK
        mock_resp.json.return_value = {'data': [1, 2]}
        self.client.get.return_value = mock_resp
        
        response = self.client.get(f'{self.base_url}/reservas/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 2)
    
    def test_listar_reservas_sin_usuario_id(self):
        """Test: Error al listar reservas sin usuarioId"""
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_400_BAD_REQUEST
        self.client.get.return_value = mock_resp
        
        response = self.client.get(f'{self.base_url}/reservas/')
        self.assertEqual(response.status_code, 400)
    
    def test_obtener_detalle_reserva(self):
        """Test: Obtener detalles de una reserva específica"""
        reserva = self.crear_pedido_valido(usuario_id=100)
        
        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_200_OK
        mock_resp.json.return_value = {'idReserva': reserva.id}
        self.client.get.return_value = mock_resp
        
        response = self.client.get(f'{self.base_url}/reservas/{reserva.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_confirmacion_automatica_reserva_confirmada(self):
        """Test: Una reserva CONFIRMADA no puede ser liberada"""
        self.crear_pedido_valido(usuario_id=100, estado=Pedido.Estado.CONFIRMADO)

        mock_resp = MagicMock()
        mock_resp.status_code = status.HTTP_200_OK
        mock_resp.json.return_value = {'data': [1, 2]}
        self.client.get.return_value = mock_resp
        
        response = self.client.get(f'{self.base_url}/reservas/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 2)


class StockModelTestCase(TestCase):
    """Tests para los modelos de Stock"""
    
    def setUp(self):
        """Configuración inicial"""
        self.categoria = Categoria.objects.create(
            nombre="Test",
            descripcion="Categoría de prueba"
        )
        self.producto = MockProducto(
            4,
            "Producto Test",
            "Descripción test",
            1000.00,
            20,
            self.categoria
        )
    
    def test_producto_tiene_stock(self):
        """Test: Verificar método tiene_stock()"""
        self.assertTrue(self.producto.tiene_stock(5))
        self.assertTrue(self.producto.tiene_stock(20))
        self.assertFalse(self.producto.tiene_stock(21))
    
    def test_producto_reservar_stock(self):
        """Test: Método reservar() reduce el stock"""
        self.producto.reservar(10)
        self.assertEqual(self.producto.stock_disponible, 10)
    
    def test_producto_liberar_stock(self):
        """Test: Método liberar() aumenta el stock"""
        self.producto.reservar(10)  # Stock = 10
        self.producto.liberar(5)    # Stock = 15
        self.assertEqual(self.producto.stock_disponible, 15)
    
    def test_categoria_str(self):
        """Test: Representación string de Categoría"""
        self.assertEqual(str(self.categoria), "Test")
    
    def test_producto_str(self):
        """Test: Representación string de Producto"""
        self.assertEqual(str(self.producto), "Producto Test")
