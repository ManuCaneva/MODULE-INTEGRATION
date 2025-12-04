"""
Script para crear pedidos de prueba usando productos reales de la API de Stock
"""
import os
import django
import sys
from decimal import Decimal
import random

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.modulos.pedidos.models import Pedido, DetallePedido, DireccionEnvio
from utils.apiCliente.stock import StockClient
from django.utils import timezone
import requests

User = get_user_model()

def obtener_productos_stock():
    """Obtiene productos de la API de Stock"""
    try:
        from django.conf import settings
        client = StockClient(settings.STOCK_API_BASE_URL)
        productos = client.listar_productos(limit=50)
        print(f"✅ Se obtuvieron {len(productos)} productos de Stock")
        if productos:
            print(f"   Ejemplo de producto: {productos[0]}")
        return productos
    except Exception as e:
        print(f"❌ Error al obtener productos de Stock: {e}")
        import traceback
        traceback.print_exc()
        return []

def crear_pedidos_prueba():
    """Crea pedidos de prueba con productos reales"""
    
    # Obtener el usuario que se autenticó más recientemente (last_login más reciente)
    usuario = User.objects.filter(last_login__isnull=False).order_by('-last_login').first()
    
    if not usuario:
        print("❌ No hay usuarios autenticados en el sistema.")
        print("   Por favor, inicia sesión en la aplicación primero.")
        return
    
    print(f"✅ Usuario autenticado más reciente: {usuario.username} (ID: {usuario.id})")
    print(f"   Último login: {usuario.last_login}")
    
    # Crear un usuario diferente para prueba
    usuario_otro, created = User.objects.get_or_create(username='otro_usuario_test')
    print(f"✅ Usuario de prueba: {usuario_otro.username} (ID: {usuario_otro.id}) - {'Creado' if created else 'Ya existía'}")
    
    # Obtener productos de Stock
    productos = obtener_productos_stock()
    
    if not productos:
        print("❌ No hay productos disponibles. Abortando...")
        return
    
    # Crear pedidos de prueba con diferentes estados
    estados_posibles = ['borrador', 'pendiente', 'confirmado', 'cancelado']
    
    print("\n🔹 Creando 3 pedidos para tu usuario...")
    for i in range(3):
        try:
            # Seleccionar productos aleatorios
            num_productos = random.randint(1, min(3, len(productos)))
            productos_pedido = random.sample(productos, num_productos)
            
            # Calcular total sumando los precios reales
            total = Decimal('0.00')
            detalles_info = []
            
            for producto in productos_pedido:
                cantidad = random.randint(1, 3)
                precio = Decimal(str(producto.get('precio', 0)))
                subtotal = precio * cantidad
                total += subtotal
                detalles_info.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'precio': precio,
                    'subtotal': subtotal
                })
            
            # Crear dirección de envío
            direccion = DireccionEnvio.objects.create(
                calle=f"Calle Falsa {random.randint(100, 999)}",
                ciudad="Resistencia",
                provincia="Chaco",
                codigo_postal="3500",
                pais="Argentina"
            )
            
            # Crear pedido con el total correcto
            pedido = Pedido.objects.create(
                usuario=usuario,
                total=total,
                estado=random.choice(estados_posibles),
                direccion_envio=direccion,
                tipo_transporte=random.choice(['air', 'sea', 'road'])
            )
            
            # Crear detalles del pedido con precios reales
            for detalle in detalles_info:
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto_id=detalle['producto'].get('id'),
                    nombre_producto=detalle['producto'].get('nombre', 'Producto'),
                    cantidad=detalle['cantidad'],
                    precio_unitario=detalle['precio']
                )
            
            print(f"✅ Pedido #{pedido.id} creado - Estado: {pedido.estado} - Total: ${pedido.total}")
            productos_nombres = ', '.join([d['producto'].get('nombre', 'N/A') for d in detalles_info])
            print(f"   Productos: {productos_nombres}")
            
        except Exception as e:
            print(f"❌ Error al crear pedido {i+1}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🔸 Creando 2 pedidos para otro usuario (NO deberían aparecer en tu lista)...")
    for i in range(2):
        try:
            # Seleccionar productos aleatorios
            num_productos = random.randint(1, min(3, len(productos)))
            productos_pedido = random.sample(productos, num_productos)
            
            # Calcular total sumando los precios reales
            total = Decimal('0.00')
            detalles_info = []
            
            for producto in productos_pedido:
                cantidad = random.randint(1, 3)
                precio = Decimal(str(producto.get('precio', 0)))
                subtotal = precio * cantidad
                total += subtotal
                detalles_info.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'precio': precio,
                    'subtotal': subtotal
                })
            
            # Crear dirección de envío
            direccion = DireccionEnvio.objects.create(
                calle=f"Calle Test {random.randint(100, 999)}",
                ciudad="Corrientes",
                provincia="Corrientes",
                codigo_postal="3400",
                pais="Argentina"
            )
            
            # Crear pedido para otro usuario
            pedido = Pedido.objects.create(
                usuario=usuario_otro,
                total=total,
                estado=random.choice(estados_posibles),
                direccion_envio=direccion,
                tipo_transporte=random.choice(['air', 'sea', 'road'])
            )
            
            # Crear detalles del pedido con precios reales
            for detalle in detalles_info:
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto_id=detalle['producto'].get('id'),
                    nombre_producto=detalle['producto'].get('nombre', 'Producto'),
                    cantidad=detalle['cantidad'],
                    precio_unitario=detalle['precio']
                )
            
            print(f"✅ Pedido #{pedido.id} creado para '{usuario_otro.username}' - Estado: {pedido.estado} - Total: ${pedido.total}")
            productos_nombres = ', '.join([d['producto'].get('nombre', 'N/A') for d in detalles_info])
            print(f"   Productos: {productos_nombres}")
            
        except Exception as e:
            print(f"❌ Error al crear pedido {i+1} para otro usuario: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🎉 Proceso completado!")
    print(f"Total de pedidos en la base de datos: {Pedido.objects.count()}")
    print(f"Pedidos para tu usuario ({usuario.username}): {Pedido.objects.filter(usuario=usuario).count()}")
    print(f"Pedidos para otro usuario ({usuario_otro.username}): {Pedido.objects.filter(usuario=usuario_otro).count()}")

if __name__ == '__main__':
    print("🚀 Iniciando creación de pedidos de prueba con productos de Stock...\n")
    crear_pedidos_prueba()
