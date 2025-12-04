import unittest
from unittest.mock import patch, Mock
import sys
from pathlib import Path

# Asegurar que el directorio del proyecto esté en sys.path para poder importar `utils` durante tests
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

# Si 'requests' no está instalado en el entorno de test, creamos un módulo falso
try:
    import requests
except Exception:
    import types, sys

    fake_requests = types.ModuleType('requests')

    class _FakeConnectionError(Exception):
        pass

    class _FakeTimeout(Exception):
        pass

    class _FakeSession:
        def __init__(self):
            pass

        def request(self, *args, **kwargs):
            raise _FakeConnectionError('no real requests')

    fake_requests.Session = lambda: _FakeSession()
    fake_requests.ConnectionError = _FakeConnectionError
    fake_requests.Timeout = _FakeTimeout
    sys.modules['requests'] = fake_requests

from utils.apiCliente.logistica import LogisticsClient
from utils.apiCliente.base import APIError


class DummyResponse:
    def __init__(self, status_code=200, json_data=None, headers=None, text=''):
        self.status_code = status_code
        self._json = json_data or {}
        self.headers = headers or {"Content-Type": "application/json"}
        self.text = text

    def json(self):
        return self._json


class TestLogisticsClient(unittest.TestCase):
    def setUp(self):
        self.client = LogisticsClient(base_url='https://api.test')

    @patch('requests.Session.request')
    def test_calculate_shipping_cost_success(self, mock_request):
        mock_request.return_value = DummyResponse(status_code=200, json_data={"total_cost": 45.5})
        res = self.client.calculate_shipping_cost({"postal_code":"H3500ABC"}, [{"id":1, "quantity":2}])
        self.assertIsInstance(res, dict)
        self.assertEqual(res.get('total_cost'), 45.5)

    @patch('requests.Session.request')
    def test_calculate_shipping_cost_unauthorized(self, mock_request):
        mock_request.return_value = DummyResponse(status_code=401, json_data={"detail":"Unauthorized"})
        with self.assertRaises(APIError) as ctx:
            self.client.calculate_shipping_cost({"postal_code":"H3500ABC"}, [{"id":1, "quantity":2}])
        self.assertEqual(ctx.exception.status, 401)

    @patch('requests.Session.request')
    def test_retry_on_connection_error(self, mock_request):
        # Simular ConnectionError en el primer intento y luego éxito
        import requests as _requests
        mock_request.side_effect = [_requests.ConnectionError('conn failed'), DummyResponse(status_code=200, json_data={"ok": True})]

        res = self.client.get('/shipping', params={})
        self.assertIsInstance(res, dict)
        self.assertTrue(res.get('ok'))

    @patch('requests.Session.request')
    def test_list_get_and_cancel_shipments(self, mock_request):
        # list_shipments
        mock_request.return_value = DummyResponse(status_code=200, json_data={"shipments": [], "pagination": {"current_page":1}})
        res = self.client.list_shipments(user_id=123)
        self.assertIn('shipments', res)

        # get_shipment
        mock_request.return_value = DummyResponse(status_code=200, json_data={"shipping_id": 789, "status": "created"})
        detail = self.client.get_shipment(789)
        self.assertEqual(detail.get('shipping_id'), 789)

        # cancel_shipment
        mock_request.return_value = DummyResponse(status_code=200, json_data={"shipping_id": 789, "status": "cancelled"})
        canceled = self.client.cancel_shipment(789)
        self.assertEqual(canceled.get('status'), 'cancelled')


if __name__ == '__main__':
    unittest.main()
