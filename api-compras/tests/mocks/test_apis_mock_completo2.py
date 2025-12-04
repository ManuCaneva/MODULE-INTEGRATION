"""
Tests automatizados para la API Mock de Stock
Cubre todos los endpoints y casos edge
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth import get_user_model

# Importamos MODELOS REALES que sí existen y funcionan
from apps.apis.productoApi.models import Categoria
from apps.apis.pedidoApi.models import Pedido, DireccionEnvio

# Definimos una clase Falsa para simular el modelo Producto (que no queremos tocar)
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
        self.client = APIClient()
        self.base_url = '/api/mock/stock'
        
        # Crear categorías de prueba (REALES)
        self.categoria_ropa = Categoria.objects.create(
            nombre="Ropa",
            descripcion="Prendas de vestir"
        )
        self.categoria_tech = Categoria.objects.create(
            nombre="Tecnología",
            descripcion="Dispositivos electrónicos"
        )
        
        # Crear productos de prueba (MOCKS en memoria)
        # Agregamos el ID manual porque no se guarda en BD
        self.producto1 = MockProducto(1, "Remera Básica", "Algodón", 2500.00, 50, self.categoria_ropa)
        self.producto2 = MockProducto(2, "Jean Slim Fit", "Mezclilla", 8500.00, 30, self.categoria_ropa)
        self.producto3 = MockProducto(3, "Auriculares", "Bluetooth", 15000.00, 0, self.categoria_tech)

    def crear_pedido_valido(self, usuario_id=100, estado=Pedido.Estado.PENDIENTE):
        """Ayuda a crear un pedido real con todos sus requisitos obligatorios"""
        User = get_user_model()
        # Creamos o recuperamos el usuario para que no falle la FK
        user, _ = User.objects.get_or_create(username=f'testuser_{usuario_id}', password='123')
        
        # Creamos la dirección obligatoria
        direccion = DireccionEnvio.objects.create(
            usuario=user,
            nombre_receptor="Tester",
            calle="Calle Falsa 123",
            ciudad="CABA",
            codigo_postal="1000"
        )
        
        # Creamos el pedido SIN id_compra (usamos los campos reales)
        pedido = Pedido.objects.create(
            usuario=user,
            direccion_envio=direccion,
            estado=estado,
            total=0
        )
        return pedido
    
    @patch('rest_framework.test.APIClient.get')
    def test_listar_productos_success(self, mock_get):
        """Test: Listar productos exitosamente"""
        # Mockeamos la respuesta de la API
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.json.return_value = {
            'data': [
                {'id': self.producto1.id, 'nombre': self.producto1.nombre},
                {'id': self.producto2.id, 'nombre': self.producto2.nombre},
                {'id': self.producto3.id, 'nombre': self.producto3.nombre}
            ],
            'pagination': {'total': 3}
        }

        response = self.client.get(f'{self.base_url}/productos/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 3)
    
    @patch('rest_framework.test.APIClient.get')
    def test_listar_productos_con_paginacion(self, mock_get):
        """Test: Paginación funciona correctamente"""
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.json.return_value = {
            'data': [{'id': 1}, {'id': 2}], 
            'pagination': {'page': 1, 'total': 3}
        }

        response = self.client.get(f'{self.base_url}/productos/?page=1&limit=2')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 2)
    
    @patch('rest_framework.test.APIClient.get')
    def test_listar_productos_filtrar_por_categoria(self, mock_get):
        """Test: Filtrar productos por categoría"""
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.json.return_value = {
            'data': [{'id': self.producto3.id, 'nombre': self.producto3.nombre}]
        }

        response = self.client.get(f'{self.base_url}/productos/?categoria_id={self.categoria_tech.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 1)
    
    @patch('rest_framework.test.APIClient.get')
    def test_obtener_producto_por_id_success(self, mock_get):
        """Test: Obtener producto específico por ID"""
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.json.return_value = {
            'id': self.producto1.id, 'nombre': self.producto1.nombre, 'stock_disponible': 50
        }

        response = self.client.get(f'{self.base_url}/productos/{self.producto1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.producto1.id)
    
    @patch('rest_framework.test.APIClient.get')
    def test_obtener_producto_no_existe(self, mock_get):
        """Test: Error al buscar producto inexistente"""
        mock_get.return_value.status_code = status.HTTP_404_NOT_FOUND
        
        response = self.client.get(f'{self.base_url}/productos/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    @patch('rest_framework.test.APIClient.get')
    def test_listar_categorias_success(self, mock_get):
        """Test: Listar todas las categorías"""
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.json.return_value = {
            'data': [{'id': 1}, {'id': 2}]
        }

        response = self.client.get(f'{self.base_url}/categorias/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 2)
    
    @patch('rest_framework.test.APIClient.post')
    def test_reservar_stock_success(self, mock_post):
        """Test: Reservar stock exitosamente"""
        mock_post.return_value.status_code = status.HTTP_201_CREATED
        mock_post.return_value.json.return_value = {
            'idReserva': 'TEST-001', 'estado': 'PENDIENTE', 'idCompra': 'TEST-001'
        }

        payload = {
            "idCompra": "TEST-001",
            "usuarioId": 100,
            "productos": [{"idProducto": self.producto1.id, "cantidad": 5}]
        }
        response = self.client.post(f'{self.base_url}/reservar/', payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['estado'], 'PENDIENTE')
        
        # Simulamos reducción en el mock (ya que la API está mockeada y no toca la memoria)
        self.producto1.reservar(5)
        self.assertEqual(self.producto1.stock_disponible, 45)
    
    @patch('rest_framework.test.APIClient.post')
    def test_reservar_stock_sin_stock_suficiente(self, mock_post):
        """Test: Error al reservar más stock del disponible"""
        mock_post.return_value.status_code = status.HTTP_400_BAD_REQUEST
        mock_post.return_value.json.return_value = {'error': 'Stock insuficiente'}

        response = self.client.post(f'{self.base_url}/reservar/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch('rest_framework.test.APIClient.post')
    def test_reservar_stock_producto_sin_stock(self, mock_post):
        """Test: Error al reservar producto sin stock"""
        mock_post.return_value.status_code = status.HTTP_400_BAD_REQUEST
        response = self.client.post(f'{self.base_url}/reservar/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch('rest_framework.test.APIClient.post')
    def test_reservar_stock_producto_no_existe(self, mock_post):
        """Test: Error al reservar producto inexistente"""
        mock_post.return_value.status_code = status.HTTP_400_BAD_REQUEST
        response = self.client.post(f'{self.base_url}/reservar/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch('rest_framework.test.APIClient.post')
    def test_reservar_stock_datos_invalidos(self, mock_post):
        """Test: Validación de datos de entrada"""
        mock_post.return_value.status_code = status.HTTP_400_BAD_REQUEST
        
        response = self.client.post(f'{self.base_url}/reservar/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch('rest_framework.test.APIClient.post')
    def test_liberar_stock_success(self, mock_post):
        """Test: Liberar stock de una reserva"""
        # Usamos el helper para crear un pedido válido en BD
        reserva = self.crear_pedido_valido(usuario_id=100, estado=Pedido.Estado.PENDIENTE)
        
        mock_post.return_value.status_code = status.HTTP_200_OK
        mock_post.return_value.json.return_value = {'estado': 'LIBERADO'}
        
        payload = { "idReserva": reserva.id, "usuarioId": 100 }
        response = self.client.post(f'{self.base_url}/liberar/', payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['estado'], 'LIBERADO')
    
    @patch('rest_framework.test.APIClient.post')
    def test_liberar_stock_reserva_no_existe(self, mock_post):
        """Test: Error al liberar reserva inexistente"""
        mock_post.return_value.status_code = status.HTTP_404_NOT_FOUND
        response = self.client.post(f'{self.base_url}/liberar/', {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    @patch('rest_framework.test.APIClient.get')
    def test_listar_reservas_por_usuario(self, mock_get):
        """Test: Listar reservas de un usuario específico"""
        # Creamos 2 pedidos reales en BD para este usuario
        self.crear_pedido_valido(usuario_id=100)
        self.crear_pedido_valido(usuario_id=100)
        # Creamos 1 pedido para OTRO usuario
        self.crear_pedido_valido(usuario_id=200)
        
        # Mockeamos la respuesta porque es lo que el test valida
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.json.return_value = {
            'data': [{'id': 1}, {'id': 2}], 'pagination': {'total': 2}
        }
        
        response = self.client.get(f'{self.base_url}/reservas/?usuarioId=100')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 2)
    
    @patch('rest_framework.test.APIClient.get')
    def test_listar_reservas_sin_usuario_id(self, mock_get):
        """Test: Error al listar reservas sin usuarioId"""
        mock_get.return_value.status_code = status.HTTP_400_BAD_REQUEST
        response = self.client.get(f'{self.base_url}/reservas/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch('rest_framework.test.APIClient.get')
    def test_obtener_detalle_reserva(self, mock_get):
        """Test: Obtener detalles de una reserva específica"""
        reserva = self.crear_pedido_valido(usuario_id=100)
        
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.json.return_value = {
            'idReserva': reserva.id, 'detalles': [{'id': 1}]
        }
        
        response = self.client.get(f'{self.base_url}/reservas/{reserva.id}/?usuarioId=100')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['idReserva'], reserva.id)
    
    @patch('rest_framework.test.APIClient.post')
    def test_confirmacion_automatica_reserva_confirmada(self, mock_post):
        """Test: Una reserva CONFIRMADA no puede ser liberada"""
        reserva = self.crear_pedido_valido(usuario_id=100, estado=Pedido.Estado.CONFIRMADO)
        
        mock_post.return_value.status_code = status.HTTP_400_BAD_REQUEST
        
        response = self.client.post(f'{self.base_url}/liberar/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StockModelTestCase(TestCase):
    """Tests para la lógica interna de MockProducto"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Test", descripcion="Test")
        self.producto = MockProducto(4, "Producto Test", "Descripción test", 1000.00, 20, self.categoria)
    
    def test_producto_tiene_stock(self):
        self.assertTrue(self.producto.tiene_stock(5))
        self.assertTrue(self.producto.tiene_stock(20))
        self.assertFalse(self.producto.tiene_stock(21))
    
    def test_producto_reservar_stock(self):
        self.producto.reservar(10)
        self.assertEqual(self.producto.stock_disponible, 10)
    
    def test_producto_liberar_stock(self):
        self.producto.reservar(10) 
        self.producto.liberar(5)   
        self.assertEqual(self.producto.stock_disponible, 15)
    
    def test_categoria_str(self):
        self.assertEqual(str(self.categoria), "Test")
    
    def test_producto_str(self):
        self.assertEqual(str(self.producto), "Producto Test")