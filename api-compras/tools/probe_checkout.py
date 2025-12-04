import os
import django
import json
import sys

# Ensure project root is on sys.path so Django settings module 'Main' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
# Create or get a probe user
user, created = User.objects.get_or_create(username='probeuser', defaults={'email': 'probe@example.com'})
if created:
    user.set_password('probe123')
    user.save()

client = Client()
# Ensure the app will call the local mock endpoints under /api/mock/stock
from django.conf import settings as djsettings
djsettings.STOCK_API_BASE_URL = djsettings.STOCK_API_BASE_URL.rstrip('/') + '/api/mock/stock'
# Prefer force_login to avoid dealing with auth backend
client.force_login(user)

payload = {
    "deliveryAddress": {
        "nombre_receptor": "Probe User",
        "calle": "Calle Falsa 123",
        "ciudad": "Ciudad",
        "provincia": "Provincia",
        "codigo_postal": "0000",
        "pais": "Argentina",
        "telefono": "3410000000",
        "informacion_adicional": "Prueba"
    },
    "products": [
        {"productId": 1, "quantity": 1},
        {"productId": 2, "quantity": 2}
    ],
    "transport_type": "domicilio",
    "payment_method": "card",
    "idCompra": "probe-12345"
}

resp = client.post('/pedidos/api/checkout/confirm/', data=json.dumps(payload), content_type='application/json')
print('STATUS', resp.status_code)
try:
    print('JSON:', json.dumps(resp.json(), indent=2, ensure_ascii=False))
except Exception:
    print('RAW:', resp.content)
