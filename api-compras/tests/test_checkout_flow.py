from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from decimal import Decimal


class CheckoutFlowTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # No dependemos de apps.apis.stockApi models en este test: parcheamos los clientes HTTP
        self.mock_product = {
            'id': 1,
            'name': 'Auriculares XYZ',
            'price': 15000.00,
            'stock': 10,
        }
        # Usuario
        User = get_user_model()
        self.user = User.objects.create_user(username='buyer', password='testpass')
        # Log in via client so @login_required decorator recognizes the user
        logged = self.client.login(username='buyer', password='testpass')
        if not logged:
            # fallback to DRF's force_authenticate if session login fails
            self.client.force_authenticate(user=self.user)

    def test_checkout_confirm_success(self):
        payload = {
            "deliveryAddress": {
                "nombre_receptor": "Juan Pérez",
                "calle": "Av. Siempreviva 742",
                "ciudad": "Buenos Aires",
                "provincia": "CABA",
                "codigo_postal": "C1000",
                "pais": "Argentina",
                "telefono": "1234567890",
                "informacion_adicional": "Dejar en portería",
            },
            "products": [
                {"productId": self.mock_product['id'], "quantity": 2}
            ],
            "transport_type": "road",
            "payment_method": "card",
            "idCompra": "TEST-CHECKOUT-1",
        }

        # Parchear StockClient y LogisticsClient para simular respuestas exitosas
        with patch('utils.apiCliente.stock.StockClient') as MockStockClient, \
             patch('utils.apiCliente.logistica.LogisticsClient') as MockLogisticsClient:

            # StockClient.obtener_producto -> devuelve nuestro product
            stock_instance = MockStockClient.return_value
            stock_instance.obtener_producto.return_value = {'id': self.mock_product['id'], 'price': self.mock_product['price'], 'name': self.mock_product['name']}
            # reservar_stock devuelve objeto de reserva simulado
            stock_instance.reservar_stock.return_value = {'id': 555, 'status': 'PENDIENTE', 'products': [{'productId': 1, 'quantity': 2}]}

            # LogisticsClient.create_shipment -> devuelve objeto envio simulado
            log_instance = MockLogisticsClient.return_value
            log_instance.create_shipment.return_value = {'id': 777, 'trackingId': 'TRK-123', 'status': 'PENDIENTE'}

            response = self.client.post('/pedidos/api/checkout/confirm/', payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            data = response.json()
            self.assertIn('pedido', data)
            self.assertIn('reserva', data)
            self.assertIn('envio', data)

    def test_checkout_reservation_insufficient_stock(self):
        # Intentar reservar más que el stock disponible
        payload = {
            "deliveryAddress": {
                "nombre_receptor": "María López",
                "calle": "Calle Falsa 123",
                "ciudad": "Rosario",
                "provincia": "Santa Fe",
                "codigo_postal": "S2000",
                "pais": "Argentina",
                "telefono": "0987654321",
            },
            "products": [
                {"productId": self.mock_product['id'], "quantity": 999}
            ],
            "transport_type": "road",
            "payment_method": "card",
            "idCompra": "TEST-CHECKOUT-FAIL",
        }

        with patch('utils.apiCliente.stock.StockClient') as MockStockClient:
            stock_instance = MockStockClient.return_value
            # Simular que reservar_stock lanza APIError
            from utils.apiCliente.base import APIError
            stock_instance.reservar_stock.side_effect = APIError('Insufficient stock', status=400, payload={'error': 'Stock insuficiente'})

            response = self.client.post('/pedidos/api/checkout/confirm/', payload, format='json')
            # Debe fallar la reserva y devolver 409 (conflicto / stock insuficiente)
            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
            data = response.json()
            self.assertIn('error', data)
            self.assertTrue('Reserva' in data['error'] or 'stock' in data.get('detail', '').lower())
