"""
Script para crear pedidos de prueba en la base de datos de Django.
Ejecutar: docker exec 2025-04-tpi-django-1 python crear_pedidos_prueba.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.modulos.pedidos.models import Pedido, DetallePedido
from decimal import Decimal

User = get_user_model()

# Obtener el usuario
try:
    usuario = User.objects.get(username='user')
except User.DoesNotExist:
    print("❌ Usuario 'user' no encontrado")
    exit(1)

print(f"✅ Usuario encontrado: {usuario.username} (ID: {usuario.id})")

# Crear 3 pedidos de prueba
pedidos_data = [
    {
        "estado": "confirmado",
        "total": Decimal("4500.00"),
        "direccion_envio": "Av. Siempre Viva 742, Springfield",
        "tipo_transporte": "road",
        "items": [
            {"producto_id": 1, "nombre": "Laptop Pro X", "cantidad": 1, "precio_unitario": Decimal("4500.00")}
        ]
    },
    {
        "estado": "en_transito",
        "total": Decimal("1200.50"),
        "direccion_envio": "Calle Falsa 123, Ciudad",
        "tipo_transporte": "air",
        "items": [
            {"producto_id": 2, "nombre": "Mouse Gaming", "cantidad": 2, "precio_unitario": Decimal("600.25")}
        ]
    },
    {
        "estado": "entregado",
        "total": Decimal("850.00"),
        "direccion_envio": "Ruta 9 Km 1520, Resistencia",
        "tipo_transporte": "sea",
        "items": [
            {"producto_id": 3, "nombre": "Teclado Mecánico", "cantidad": 1, "precio_unitario": Decimal("850.00")}
        ]
    },
]

print("\n📦 Creando pedidos de prueba...\n")

for i, data in enumerate(pedidos_data, 1):
    pedido = Pedido.objects.create(
        usuario=usuario,
        estado=data["estado"],
        total=data["total"],
        direccion_envio=data["direccion_envio"],
        tipo_transporte=data.get("tipo_transporte", "road")
    )
    
    for item in data["items"]:
        DetallePedido.objects.create(
            pedido=pedido,
            producto_id=item["producto_id"],
            nombre_producto=item["nombre"],
            cantidad=item["cantidad"],
            precio_unitario=item["precio_unitario"]
        )
    
    print(f"✅ Pedido #{pedido.id} creado: {pedido.estado} - ${pedido.total}")

print(f"\n🎉 Se crearon {len(pedidos_data)} pedidos de prueba exitosamente!")
print(f"👤 Usuario: {usuario.username}")
