# Planificación: APIs Mock de Stock y Logística

**Fecha:** 16 de octubre de 2025  
**Proyecto:** DesarrolloAPP  
**Branch:** api  
**Autor:** Equipo Backend

---

## 📋 Objetivo

Crear dos **APIs simuladas/mock** dentro del proyecto Django que **repliquen exactamente el comportamiento de las APIs externas** de **Stock** y **Logística**. Estas APIs permitirán:

1. **Desarrollo independiente**: Trabajar sin depender de servicios externos
2. **Testing completo**: Probar el sistema de extremo a extremo
3. **Datos de prueba controlados**: Generar escenarios específicos (productos agotados, errores, etc.)
4. **Desarrollo offline**: No requiere conexión con servicios externos
5. **Switch fácil**: Cambiar entre APIs mock (desarrollo) y reales (producción) mediante configuración

---

## 🏗️ Arquitectura Propuesta

```
┌─────────────────────────────────────────────────────────┐
│              Tu Aplicación Backend Django                │
│                                                           │
│  ┌────────────────────┐      ┌─────────────────────┐   │
│  │  Módulo Pedidos    │      │  Módulo Carrito     │   │
│  │  Módulo Admin      │      │  Otros módulos      │   │
│  └─────────┬──────────┘      └──────────┬──────────┘   │
│            │                            │               │
│            └────────────┬───────────────┘               │
│                         │                               │
│                         ▼                               │
│            ┌────────────────────────┐                   │
│            │   StockClient          │                   │
│            │   LogisticsClient      │                   │
│            │   (utils/apiCliente)   │                   │
│            └─────────┬──────────────┘                   │
└──────────────────────┼──────────────────────────────────┘
                       │
                       │ ◄─── Apunta aquí según settings
                       │
        ┌──────────────┴─────────────┐
        │                            │
        ▼ DESARROLLO                 ▼ PRODUCCIÓN
┌─────────────────────┐      ┌─────────────────────┐
│  APIs Mock (Django) │      │  APIs Externas      │
│                     │      │  Reales             │
│  /api/mock/stock/   │      │  https://stock.     │
│  /api/mock/         │      │  external.com       │
│  logistica/         │      │                     │
│                     │      │  https://logistics. │
│  • BD SQLite local  │      │  external.com       │
│  • Datos de prueba  │      │                     │
│  • Respuestas rápidas│     │  • Servicios reales │
└─────────────────────┘      └─────────────────────┘
```

### 🔄 Switch entre Desarrollo y Producción

En `settings.py`:
```python
# Desarrollo: usar APIs mock locales
USE_MOCK_APIS = True  
STOCK_API_BASE_URL = "http://localhost:8000/api/mock/stock"
LOGISTICS_API_BASE_URL = "http://localhost:8000/api/mock/logistica"

# Producción: usar APIs externas reales
# USE_MOCK_APIS = False
# STOCK_API_BASE_URL = "https://stock-api-externa.com/api"
# LOGISTICS_API_BASE_URL = "https://logistics-api-externa.com/api"
```

---

## 📁 Estructura de Archivos

```
DesarrolloAPP/
└── apps/
    └── apis/
        ├── stockApi/               # API Mock de Stock
        │   ├── __init__.py
        │   ├── models.py          # Modelos: Producto, Categoria, Reserva
        │   ├── views.py           # ViewSets que simulan API externa
        │   ├── serializers.py     # Schemas idénticos a API externa
        │   ├── urls.py            # URLs: /api/mock/stock/...
        │   ├── admin.py           # Admin para gestionar datos de prueba
        │   ├── fixtures.py        # Datos de prueba iniciales
        │   └── tests.py           # Tests
        │
        └── logisticaApi/          # API Mock de Logística
            ├── __init__.py
            ├── models.py          # Modelos: Envio, MetodoTransporte
            ├── views.py           # ViewSets que simulan API externa
            ├── serializers.py     # Schemas idénticos a API externa
            ├── urls.py            # URLs: /api/mock/logistica/...
            ├── admin.py           # Admin para gestionar datos de prueba
            ├── fixtures.py        # Datos de prueba iniciales
            └── tests.py           # Tests
```

---

## 🎯 API Mock: Stock

### Endpoints a Implementar (Réplica Exacta)

| Método | Endpoint | Descripción | Respuesta Mock |
|--------|----------|-------------|----------------|
| `GET` | `/api/mock/stock/productos/` | Listar productos | Lista paginada de BD local |
| `GET` | `/api/mock/stock/productos/{id}/` | Detalle de producto | Producto de BD local |
| `POST` | `/api/mock/stock/stock/reservar/` | Reservar stock | Crea reserva en BD, reduce stock |
| `GET` | `/api/mock/stock/reservas/` | Listar reservas | Reservas del usuario |
| `GET` | `/api/mock/stock/reservas/{id}/` | Detalle de reserva | Reserva específica |
| `POST` | `/api/mock/stock/stock/liberar/` | Liberar stock | Cancela reserva, restaura stock |
| `GET` | `/api/mock/stock/categorias/` | Listar categorías | Lista de BD local |
| `GET` | `/api/mock/stock/categorias/{id}/` | Detalle categoría | Categoría específica |

### Modelos de Datos (models.py)

```python
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        db_table = 'mock_categoria'
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_disponible = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen_url = models.URLField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'mock_producto'
    
    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock_disponible})"

class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('expirada', 'Expirada'),
    ]
    
    id_compra = models.CharField(max_length=100, unique=True)
    usuario_id = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()  # Ej: +15 minutos
    
    class Meta:
        db_table = 'mock_reserva'
    
    def __str__(self):
        return f"Reserva {self.id_compra} - {self.estado}"

class DetalleReserva(models.Model):
    reserva = models.ForeignKey(Reserva, related_name='productos', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'mock_detalle_reserva'
```

### Comportamiento Mock

- **Validación realista**: Verificar que hay stock suficiente antes de reservar
- **Estados**: Las reservas pueden estar pendientes, confirmadas o expiradas
- **Atomicidad**: Reservar reduce el stock disponible
- **Errores simulados**: Retornar 404 si producto no existe, 400 si no hay stock

---

## 🚚 API Mock: Logística

### Endpoints a Implementar (Réplica Exacta)

| Método | Endpoint | Descripción | Respuesta Mock |
|--------|----------|-------------|----------------|
| `POST` | `/api/mock/logistica/shipping/cost/` | Calcular costo de envío | Cálculo simulado basado en peso/distancia |
| `GET` | `/api/mock/logistica/shipping/transport-methods/` | Métodos disponibles | Lista hardcoded (air, road, rail, sea) |
| `POST` | `/api/mock/logistica/shipping/` | Crear envío | Crea registro en BD con estado "pendiente" |
| `GET` | `/api/mock/logistica/shipping/` | Listar envíos | Lista paginada de BD local |
| `GET` | `/api/mock/logistica/shipping/{id}/` | Detalle de envío | Envío específico de BD |
| `POST` | `/api/mock/logistica/shipping/{id}/cancel/` | Cancelar envío | Cambia estado a "cancelado" |

### Modelos de Datos (models.py)

```python
from django.db import models
import json

class MetodoTransporte(models.Model):
    TIPOS = [
        ('air', 'Aéreo'),
        ('road', 'Terrestre'),
        ('rail', 'Ferroviario'),
        ('sea', 'Marítimo'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPOS, unique=True)
    nombre_display = models.CharField(max_length=100)
    tiempo_estimado_dias = models.IntegerField()
    costo_base = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'mock_metodo_transporte'
    
    def __str__(self):
        return self.nombre_display

class Envio(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En Preparación'),
        ('en_transito', 'En Tránsito'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    order_id = models.IntegerField()
    user_id = models.IntegerField()
    
    # Dirección (guardada como JSON para simplicidad)
    direccion_calle = models.CharField(max_length=200)
    direccion_ciudad = models.CharField(max_length=100)
    direccion_estado = models.CharField(max_length=100)
    direccion_codigo_postal = models.CharField(max_length=20)
    direccion_pais = models.CharField(max_length=100)
    
    metodo_transporte = models.ForeignKey(MetodoTransporte, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_estimada_entrega = models.DateTimeField(null=True, blank=True)
    fecha_entrega_real = models.DateTimeField(null=True, blank=True)
    
    tracking_number = models.CharField(max_length=50, unique=True, blank=True)
    
    class Meta:
        db_table = 'mock_envio'
    
    def __str__(self):
        return f"Envío #{self.id} - Orden #{self.order_id}"

class ProductoEnvio(models.Model):
    envio = models.ForeignKey(Envio, related_name='productos', on_delete=models.CASCADE)
    producto_id = models.IntegerField()
    cantidad = models.IntegerField()
    
    class Meta:
        db_table = 'mock_producto_envio'
```

### Comportamiento Mock

- **Cálculo de costos**: Fórmula simple basada en cantidad de productos y tipo de transporte
- **Tracking number**: Generado automáticamente (ej: `SHIP-{timestamp}-{id}`)
- **Cambio de estados**: Simular progresión de estados (pendiente → en_preparacion → en_transito → entregado)
- **Validaciones**: No se puede cancelar un envío ya entregado
- **Fecha estimada**: Calculada automáticamente según método de transporte

---

## 🔧 Tecnologías y Herramientas

- **Framework**: Django REST Framework (DRF)
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Serializers**: DRF Serializers (schemas idénticos a APIs externas)
- **Autenticación**: Opcional para APIs mock (pueden ser públicas en dev)
- **Admin**: Django Admin para gestionar datos de prueba fácilmente
- **Fixtures**: JSON fixtures para poblar datos iniciales
- **Documentación**: drf-spectacular (OpenAPI/Swagger)
- **Testing**: pytest-django para probar las APIs mock

---

## 📊 Ventajas de APIs Mock

### ✅ **Beneficios para el Desarrollo**

1. **Desarrollo paralelo**: Frontend y backend pueden trabajar simultáneamente
2. **Testing realista**: Probar flujos completos sin servicios externos
3. **Datos controlados**: Crear escenarios específicos (errores, productos agotados, etc.)
4. **Velocidad**: Respuestas instantáneas sin latencia de red
5. **Offline**: Trabajar sin conexión a internet
6. **Costos**: No consume recursos de APIs externas (que podrían tener límites/costos)
7. **Estabilidad**: No depender de disponibilidad de servicios externos
8. **Debugging**: Más fácil debuggear problemas en tu entorno controlado

### 🎭 Escenarios de Prueba Posibles

Con APIs mock puedes simular:
- ✅ Productos con stock bajo o agotado
- ✅ Reservas que expiran
- ✅ Errores de red (timeouts, 500)
- ✅ Cambios de precios dinámicos
- ✅ Envíos cancelados o retrasados
- ✅ Diferentes métodos de pago/transporte
- ✅ Múltiples usuarios comprando el mismo producto

---

## 🚀 Plan de Implementación

### Fase 1: Configuración Inicial (1 día)
- [ ] Crear carpetas `apps/apis/stockApi/` y `apps/apis/logisticaApi/`
- [ ] Agregar apps a `INSTALLED_APPS` en settings.py
- [ ] Configurar variables `USE_MOCK_APIS`, `STOCK_API_BASE_URL`, etc.
- [ ] Crear archivos base: `__init__.py`, `models.py`, `views.py`, etc.

### Fase 2: Stock API Mock (2-3 días)
- [ ] Crear modelos: Categoria, Producto, Reserva, DetalleReserva
- [ ] Crear serializers que repliquen schemas de API externa
- [ ] Implementar ViewSets para todos los endpoints
- [ ] Configurar URLs: `/api/mock/stock/...`
- [ ] Crear fixtures con datos de prueba (20-30 productos)
- [ ] Configurar Django Admin para gestión de datos
- [ ] Probar endpoints con Postman/curl

### Fase 3: Logística API Mock (2-3 días)
- [ ] Crear modelos: MetodoTransporte, Envio, ProductoEnvio
- [ ] Crear serializers que repliquen schemas de API externa
- [ ] Implementar ViewSets para todos los endpoints
- [ ] Configurar URLs: `/api/mock/logistica/...`
- [ ] Crear fixtures con métodos de transporte
- [ ] Implementar lógica de cálculo de costos
- [ ] Configurar Django Admin
- [ ] Probar endpoints

### Fase 4: Integración y Testing (1-2 días)
- [ ] Actualizar `StockClient` y `LogisticsClient` para usar URLs de settings
- [ ] Crear comando management para poblar datos de prueba
- [ ] Escribir tests unitarios para ambas APIs
- [ ] Crear documentación OpenAPI/Swagger
- [ ] Probar flujo completo: reservar → crear envío → cancelar
- [ ] Documentar cómo cambiar entre mock y real

### Fase 5: Extras Opcionales (1 día)
- [ ] Agregar endpoint para simular errores (/api/mock/simulate-error/)
- [ ] Implementar delays artificiales para simular latencia de red
- [ ] Agregar dashboard de admin para ver estadísticas de uso
- [ ] Crear script para resetear datos de prueba

---

## 📝 Ejemplo de Implementación

### Stock API Mock - Modelo (models.py)

```python
from django.db import models
from datetime import timedelta
from django.utils import timezone

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_disponible = models.IntegerField(default=0)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    imagen_url = models.URLField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'mock_producto'
    
    def tiene_stock(self, cantidad):
        return self.stock_disponible >= cantidad
    
    def reservar(self, cantidad):
        if self.tiene_stock(cantidad):
            self.stock_disponible -= cantidad
            self.save()
            return True
        return False
```

### Stock API Mock - Serializer (serializers.py)

```python
from rest_framework import serializers
from .models import Producto, Categoria, Reserva, DetalleReserva

class ProductoSerializer(serializers.ModelSerializer):
    """Serializer que replica el schema de la API externa"""
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 
                  'stock_disponible', 'categoria', 'imagen_url', 'activo']

class ReservaInputSerializer(serializers.Serializer):
    """Schema de entrada para reservar stock (idéntico a API externa)"""
    idCompra = serializers.CharField(max_length=100)
    usuarioId = serializers.IntegerField()
    productos = serializers.ListField(
        child=serializers.DictField()
    )
    
    def validate_productos(self, value):
        for prod in value:
            if 'idProducto' not in prod or 'cantidad' not in prod:
                raise serializers.ValidationError(
                    "Cada producto debe tener 'idProducto' y 'cantidad'"
                )
            if prod['cantidad'] <= 0:
                raise serializers.ValidationError("Cantidad debe ser > 0")
        return value

class ReservaOutputSerializer(serializers.Serializer):
    """Schema de salida (idéntico a API externa)"""
    idReserva = serializers.IntegerField()
    estado = serializers.CharField()
    mensaje = serializers.CharField()
    productos = serializers.ListField()
```

### Stock API Mock - View (views.py)

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from datetime import timedelta
from django.utils import timezone
from .models import Producto, Reserva, DetalleReserva
from .serializers import (ProductoSerializer, ReservaInputSerializer, 
                          ReservaOutputSerializer)
import logging

logger = logging.getLogger(__name__)

class StockMockViewSet(viewsets.ViewSet):
    """
    API Mock que simula el comportamiento de la API externa de Stock
    """
    
    @action(detail=False, methods=['get'], url_path='productos')
    def listar_productos(self, request):
        """GET /api/mock/stock/productos/ - Listar productos con paginación"""
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 20))
        q = request.query_params.get('q', '')
        categoria_id = request.query_params.get('categoriaId', None)
        
        queryset = Producto.objects.filter(activo=True)
        
        if q:
            queryset = queryset.filter(nombre__icontains=q)
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        
        # Paginación simple
        total = queryset.count()
        start = (page - 1) * limit
        end = start + limit
        productos = queryset[start:end]
        
        serializer = ProductoSerializer(productos, many=True)
        
        return Response({
            'data': serializer.data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        })
    
    @action(detail=False, methods=['post'], url_path='stock/reservar')
    def reservar_stock(self, request):
        """POST /api/mock/stock/stock/reservar/ - Reservar stock"""
        serializer = ReservaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        try:
            with transaction.atomic():
                # Crear reserva
                reserva = Reserva.objects.create(
                    id_compra=data['idCompra'],
                    usuario_id=data['usuarioId'],
                    estado='pendiente',
                    fecha_expiracion=timezone.now() + timedelta(minutes=15)
                )
                
                # Reservar productos
                productos_reservados = []
                for item in data['productos']:
                    producto = Producto.objects.get(id=item['idProducto'])
                    cantidad = item['cantidad']
                    
                    # Verificar stock
                    if not producto.tiene_stock(cantidad):
                        raise ValueError(
                            f"Stock insuficiente para {producto.nombre}"
                        )
                    
                    # Reservar
                    producto.reservar(cantidad)
                    
                    # Guardar detalle
                    DetalleReserva.objects.create(
                        reserva=reserva,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio
                    )
                    
                    productos_reservados.append({
                        'idProducto': producto.id,
                        'nombre': producto.nombre,
                        'cantidad': cantidad,
                        'precio': str(producto.precio)
                    })
                
                logger.info(f"Reserva creada: {reserva.id_compra}")
                
                return Response({
                    'idReserva': reserva.id,
                    'estado': reserva.estado,
                    'mensaje': 'Reserva realizada exitosamente',
                    'productos': productos_reservados
                }, status=status.HTTP_200_OK)
                
        except Producto.DoesNotExist:
            return Response({
                'error': 'Producto no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error al reservar: {str(e)}")
            return Response({
                'error': 'Error interno al procesar reserva'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

### Stock API Mock - URLs (urls.py)

```python
from django.urls import path
from .views import StockMockViewSet

# Endpoints sin router para mayor control
urlpatterns = [
    # Productos
    path('productos/', 
         StockMockViewSet.as_view({'get': 'listar_productos'}),
         name='mock-stock-productos'),
    path('productos/<int:pk>/', 
         StockMockViewSet.as_view({'get': 'obtener_producto'}),
         name='mock-stock-producto-detail'),
    
    # Reservas
    path('stock/reservar/', 
         StockMockViewSet.as_view({'post': 'reservar_stock'}),
         name='mock-stock-reservar'),
    path('reservas/', 
         StockMockViewSet.as_view({'get': 'listar_reservas'}),
         name='mock-stock-reservas'),
    
    # Categorías
    path('categorias/', 
         StockMockViewSet.as_view({'get': 'listar_categorias'}),
         name='mock-stock-categorias'),
]
```

### Configuración en Main/urls.py

```python
from django.urls import path, include

urlpatterns = [
    # ... otras URLs
    
    # APIs Mock (solo en desarrollo)
    path('api/mock/stock/', include('apps.apis.stockApi.urls')),
    path('api/mock/logistica/', include('apps.apis.logisticaApi.urls')),
]
```

### Configuración en settings.py

```python
# ==========================================
# CONFIGURACIÓN DE APIS EXTERNAS
# ==========================================

# Cambiar a False en producción para usar APIs reales
USE_MOCK_APIS = True

if USE_MOCK_APIS:
    # Desarrollo: APIs Mock locales
    STOCK_API_BASE_URL = "http://127.0.0.1:8000/api/mock/stock"
    LOGISTICS_API_BASE_URL = "http://127.0.0.1:8000/api/mock/logistica"
    print("⚠️  Usando APIs MOCK (desarrollo)")
else:
    # Producción: APIs externas reales
    STOCK_API_BASE_URL = "https://api-stock-externa.com"
    LOGISTICS_API_BASE_URL = "https://api-logistica-externa.com"
    print("✅ Usando APIs externas reales")
```

### Fixtures - Datos de Prueba (fixtures/productos.json)

```json
[
  {
    "model": "stockApi.categoria",
    "pk": 1,
    "fields": {
      "nombre": "Electrónica",
      "descripcion": "Productos electrónicos"
    }
  },
  {
    "model": "stockApi.producto",
    "pk": 1,
    "fields": {
      "nombre": "Laptop Dell XPS 13",
      "descripcion": "Laptop ultrabook de alto rendimiento",
      "precio": "1299.99",
      "stock_disponible": 15,
      "categoria": 1,
      "activo": true
    }
  },
  {
    "model": "stockApi.producto",
    "pk": 2,
    "fields": {
      "nombre": "iPhone 15 Pro",
      "descripcion": "Smartphone Apple última generación",
      "precio": "999.00",
      "stock_disponible": 0,
      "categoria": 1,
      "activo": true
    }
  }
]
```

### Comando para cargar fixtures

```bash
python manage.py loaddata apps/apis/stockApi/fixtures/productos.json
```

---

## 🔒 Consideraciones Importantes

### 1. **Datos de Prueba Realistas**
- Crear al menos 30-50 productos variados
- Incluir productos con diferentes niveles de stock (alto, bajo, agotado)
- Crear varias categorías
- Simular métodos de transporte con costos diferentes

### 2. **Comportamiento Realista**
- Reservas deben expirar después de X minutos
- Stock debe reducirse al reservar
- No permitir cancelar envíos ya entregados
- Generar tracking numbers únicos

### 3. **Errores Simulados**
Implementar endpoint para forzar errores:
```python
@action(detail=False, methods=['post'], url_path='simulate-error')
def simulate_error(self, request):
    error_type = request.data.get('type', '500')
    if error_type == '404':
        return Response({'error': 'Not found'}, status=404)
    elif error_type == '500':
        return Response({'error': 'Internal error'}, status=500)
    elif error_type == 'timeout':
        import time
        time.sleep(30)  # Simular timeout
```

### 4. **Switch Desarrollo/Producción**
```python
# En utils/apiCliente/__init__.py o similar
from django.conf import settings

def get_stock_client():
    """Factory que retorna el cliente apropiado según configuración"""
    from .stock import StockClient
    return StockClient(
        base_url=settings.STOCK_API_BASE_URL,
        timeout=8.0
    )
```

### 5. **Migraciones**
```bash
# Después de crear los modelos
python manage.py makemigrations stockApi logisticaApi
python manage.py migrate
```

### 6. **Django Admin**
Registrar modelos en admin.py para gestión fácil:
```python
from django.contrib import admin
from .models import Producto, Categoria, Reserva

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock_disponible', 'categoria', 'activo']
    list_filter = ['categoria', 'activo']
    search_fields = ['nombre']
```

---

## 🧪 Testing

### Estrategia de Tests

1. **Tests de las APIs Mock**: Verificar que responden correctamente
2. **Tests de integración**: Probar `StockClient` contra las APIs mock
3. **Tests end-to-end**: Flujo completo de compra

### Ejemplo de Test

```python
from django.test import TestCase
from rest_framework.test import APIClient
from apps.apis.stockApi.models import Producto, Categoria

class StockMockAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Crear datos de prueba
        self.categoria = Categoria.objects.create(nombre="Test")
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            precio=100.00,
            stock_disponible=10,
            categoria=self.categoria
        )
    
    def test_listar_productos(self):
        """Test GET /api/mock/stock/productos/"""
        response = self.client.get('/api/mock/stock/productos/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)
        self.assertIn('pagination', response.data)
        self.assertEqual(len(response.data['data']), 1)
    
    def test_reservar_stock_exitoso(self):
        """Test POST /api/mock/stock/stock/reservar/"""
        response = self.client.post('/api/mock/stock/stock/reservar/', {
            'idCompra': 'TEST-001',
            'usuarioId': 1,
            'productos': [
                {'idProducto': self.producto.id, 'cantidad': 2}
            ]
        }, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('idReserva', response.data)
        
        # Verificar que se redujo el stock
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_disponible, 8)
    
    def test_reservar_sin_stock(self):
        """Test reserva cuando no hay stock suficiente"""
        response = self.client.post('/api/mock/stock/stock/reservar/', {
            'idCompra': 'TEST-002',
            'usuarioId': 1,
            'productos': [
                {'idProducto': self.producto.id, 'cantidad': 20}  # Más del stock
            ]
        }, format='json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
```

### Test de Integración con StockClient

```python
from utils.apiCliente.stock import StockClient

class StockClientIntegrationTests(TestCase):
    def setUp(self):
        # Crear datos en API mock
        self.categoria = Categoria.objects.create(nombre="Test")
        self.producto = Producto.objects.create(
            nombre="Test Product",
            precio=50.00,
            stock_disponible=5,
            categoria=self.categoria
        )
        
        # Cliente apuntando a API mock
        self.client = StockClient(base_url="http://localhost:8000/api/mock/stock")
    
    def test_client_listar_productos(self):
        """Probar que el cliente funciona con la API mock"""
        resultado = self.client.listar_productos(page=1, limit=10)
        
        self.assertIn('data', resultado)
        self.assertTrue(len(resultado['data']) > 0)
```

---

## 🎓 Conclusiones

### Ventajas de APIs Mock

✅ **Desarrollo independiente**: No depender de servicios externos  
✅ **Testing realista**: Probar flujos completos sin servicios reales  
✅ **Control total**: Simular cualquier escenario (errores, delays, etc.)  
✅ **Velocidad**: Respuestas instantáneas  
✅ **Offline**: Trabajar sin internet  
✅ **Costos**: Evitar límites/costos de APIs externas  
✅ **Estabilidad**: No depender de disponibilidad externa  
✅ **Debugging**: Más fácil en entorno controlado  

### Flujo de Trabajo Recomendado

1. **Desarrollo inicial**: Usar APIs mock exclusivamente
2. **Testing local**: Probar con datos controlados
3. **Staging**: Comenzar a usar APIs reales para validar integración
4. **Producción**: APIs reales con fallback a mock en caso de falla (opcional)

### Próximos Pasos

1. ✅ Revisar y aprobar este plan con el equipo
2. Configurar entorno de desarrollo (settings.py)
3. Crear modelos y migraciones (Fase 1-2)
4. Implementar Stock API Mock (Fase 2)
5. Implementar Logística API Mock (Fase 3)
6. Crear fixtures con datos de prueba
7. Testing completo (Fase 4)
8. Documentar cómo cambiar entre mock y real

---

## 📞 Recursos Adicionales

### Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations stockApi logisticaApi

# Aplicar migraciones
python manage.py migrate

# Cargar datos de prueba
python manage.py loaddata apps/apis/stockApi/fixtures/productos.json

# Crear superusuario para acceder al admin
python manage.py createsuperuser

# Limpiar y recargar datos
python manage.py flush
python manage.py loaddata productos.json metodos_transporte.json
```

### URLs de Prueba (Desarrollo)

- Stock Mock: `http://localhost:8000/api/mock/stock/`
- Logística Mock: `http://localhost:8000/api/mock/logistica/`
- Django Admin: `http://localhost:8000/admin/`
- Swagger/OpenAPI: `http://localhost:8000/api/docs/`

### Estructura Final de URLs

```
/api/mock/stock/
    - GET  /productos/              # Listar productos
    - GET  /productos/{id}/         # Detalle producto
    - POST /stock/reservar/         # Reservar stock
    - GET  /reservas/               # Listar reservas
    - GET  /reservas/{id}/          # Detalle reserva
    - POST /stock/liberar/          # Liberar reserva
    - GET  /categorias/             # Listar categorías
    - GET  /categorias/{id}/        # Detalle categoría

/api/mock/logistica/
    - POST /shipping/cost/          # Calcular costo
    - GET  /shipping/transport-methods/ # Métodos de transporte
    - POST /shipping/               # Crear envío
    - GET  /shipping/               # Listar envíos
    - GET  /shipping/{id}/          # Detalle envío
    - POST /shipping/{id}/cancel/   # Cancelar envío
```

---

## 📚 Referencias

- **Django REST Framework**: https://www.django-rest-framework.org/
- **Django Models**: https://docs.djangoproject.com/en/stable/topics/db/models/
- **Fixtures**: https://docs.djangoproject.com/en/stable/howto/initial-data/
- **Testing**: https://docs.djangoproject.com/en/stable/topics/testing/

---

**Fin del documento**

*Última actualización: 16 de octubre de 2025*  
*Branch: api*  
*Estado: Planificación completa para APIs Mock*
