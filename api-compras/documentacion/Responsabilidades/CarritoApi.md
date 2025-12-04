# carritoApi

API REST para gestión del carrito de compras. Permite a los usuarios agregar, actualizar, eliminar y consultar productos en su carrito antes de proceder al checkout.

---

## 📁 Estructura de archivos

### **`models.py`**
Define los modelos de datos para el carrito de compras:

- **`Carrito`**: Representa el carrito asociado a un usuario
  - `usuario`: Relación ForeignKey con el modelo User
  - `creado_en`: Timestamp de creación automática
  - `actualizado_en`: Timestamp de última actualización automática

- **`ItemCarrito`**: Representa cada producto dentro del carrito
  - `carrito`: Relación ForeignKey con Carrito
  - `producto_id`: ID del producto (entero, referencia externa al módulo Stock)
  - `cantidad`: Cantidad del producto (entero positivo, default=1)
  - `agregado_en`: Timestamp de cuando se agregó al carrito

**Responsabilidad**: Persistencia de datos del carrito en base de datos PostgreSQL. No almacena información completa del producto, solo el ID y cantidad.

---

### **`serializer.py`**
Serializers para transformar objetos Django en JSON y viceversa:

- **`CartItemSerializer`**: Serializa cada ítem del carrito
  - Mapea `producto_id` → `productId` (camelCase para frontend)
  - Mapea `cantidad` → `quantity`
  - `get_product()`: Obtiene datos completos del producto desde Stock API usando `StockClient`
  - Soporta serialización por lotes (batch) para optimizar llamadas a Stock API

- **`CartSerializer`**: Serializa el carrito completo
  - Lista todos los ítems con `CartItemSerializer`
  - `get_total()`: Calcula total de ítems en el carrito

**Responsabilidad**: Transformación de datos entre formato Django ORM y JSON. Enriquece la respuesta con información de productos desde Stock API.

---

### **`views.py`**
ViewSet RESTful que expone los endpoints HTTP:

- **`CartViewSet`** (heredado de `viewsets.ViewSet`):
  - `list()` - `GET /api/shopcart/`: Obtiene el carrito con todos sus productos
  - `create()` - `POST /api/shopcart/`: Agrega un producto al carrito
  - `update()` - `PUT /api/shopcart/{productId}/`: Actualiza cantidad de un producto
  - `destroy()` - `DELETE /api/shopcart/{productId}/`: Elimina un producto del carrito
  - `destroy()` sin pk - `DELETE /api/shopcart/`: Vacía el carrito completo

**Lógica de negocio**:
- Crea carritos automáticamente si no existen (`get_or_create`)
- Valida existencia de productos consultando Stock API antes de agregar
- Maneja errores con códigos semánticos (`INVALID_DATA`, `PRODUCT_NOT_FOUND`, `CART_ITEM_NOT_FOUND`)
- Incrementa cantidad si el producto ya existe en el carrito

**Responsabilidad**: Controlador HTTP que orquesta las operaciones del carrito, valida datos y coordina con Stock API.

---

### **`client.py`**
Cliente HTTP para comunicación con APIs externas:

- **`CarritoAPIClient`** (heredado de `BaseAPIClient`):
  - `obtener_carrito(usuario_id)`: GET del carrito de un usuario
  - `obtener_items(usuario_id)`: Extrae solo la lista de ítems del carrito
  - `agregar_producto(usuario_id, producto_id, cantidad)`: POST para agregar producto
  - `actualizar_producto(usuario_id, producto_id, cantidad)`: PUT para actualizar cantidad
  - `eliminar_producto(usuario_id, producto_id)`: DELETE para remover producto
  - `vaciar_carrito(usuario_id)`: DELETE para vaciar carrito completo
  - `sincronizar_carrito(usuario_id, items)`: PUT para reemplazar todo el contenido

- **Integración con Stock API**:
  - Instancia automáticamente un `StockClient` para consultar productos
  - Configurable vía `settings.CARRITO_API_BASE_URL` y `settings.STOCK_API_BASE_URL`
  - Soporta autenticación con tokens y API keys
  - Retry automático de peticiones fallidas (hasta 2 reintentos, timeout 8s)

- **`obtener_cliente_carrito()`**: Factory function para crear instancias del cliente con configuración del proyecto

**Responsabilidad**: Abstracción de comunicación HTTP con servicios externos. Desacopla las vistas de los detalles de implementación de las APIs. Facilita testing mediante inyección de dependencias.

---

### **`urls.py`**
Configuración de rutas HTTP:

```python
router = DefaultRouter()
router.register(r'shopcart', CartViewSet, basename='shopcart')
```

**Endpoints generados automáticamente**:
- `GET    /api/shopcart/` - Ver carrito
- `POST   /api/shopcart/` - Agregar producto
- `PUT    /api/shopcart/{id}/` - Actualizar cantidad
- `DELETE /api/shopcart/{id}/` - Eliminar producto
- `DELETE /api/shopcart/` - Vaciar carrito

**Responsabilidad**: Enrutamiento de peticiones HTTP hacia el ViewSet correspondiente usando Django REST Framework Router.

---

### **`apps.py`**
Configuración de la aplicación Django:

```python
class InicioConfig(AppConfig):
    name = 'apps.apis.carritoApi'
    default_auto_field = 'django.db.models.BigAutoField'
```

**Responsabilidad**: Metadatos y configuración de la app para el registro en `INSTALLED_APPS`.

---

### **`admin.py`**
Registro de modelos en el panel de administración Django (actualmente vacío).

**Responsabilidad**: Configuración del Django Admin para gestionar carritos desde el panel web administrativo.

---

### **`tests.py`**
Archivo para pruebas unitarias e integración (actualmente con imports básicos).

**Responsabilidad**: Testing de la funcionalidad del carrito. Debe contener pruebas para validar:
- Creación de carritos
- Agregar/actualizar/eliminar productos
- Validaciones de datos
- Integración con Stock API

---

## 🔗 Dependencias externas

### **Stock API** (módulo externo)
- **Endpoint**: Configurado en `settings.STOCK_API_BASE_URL`
- **Uso**: Obtener información completa de productos (nombre, precio, stock disponible)
- **Métodos utilizados**:
  - `obtener_producto(producto_id)`: Consulta un producto específico
  - `obtener_productos_por_ids([ids])`: Batch query para múltiples productos

### **Logística API** (módulo externo)
- **No utilizada directamente** en carritoApi
- Integración en el módulo `pedidoApi` para calcular costos de envío

---

## 🔧 Configuración requerida

En `settings.py`:

```python
# URLs de servicios externos
STOCK_API_BASE_URL = 'http://localhost:8001/api/'
CARRITO_API_BASE_URL = 'http://localhost:8000/api/'

# Configuración de cliente HTTP
CARRITO_CLIENT_TIMEOUT = 8.0
CARRITO_CLIENT_MAX_RETRIES = 2
```

---

## 📊 Flujo de datos

```
Usuario → Frontend → CartViewSet → models.Carrito/ItemCarrito
                         ↓
                    StockClient → Stock API (validar producto)
                         ↓
                    CartSerializer → JSON Response
```

---

## 🧪 Testing

Para ejecutar las pruebas del módulo:

```powershell
python manage.py test apps.apis.carritoApi
```

---

## 📝 Notas de implementación

1. **IDs de producto externos**: El carrito solo almacena `producto_id` (entero), la información completa se obtiene dinámicamente de Stock API

2. **Carrito anónimo**: Actualmente requiere usuario autenticado. Para soportar usuarios anónimos, el campo `usuario` en `Carrito` es nullable (`blank=True, null=True`)

3. **Optimización de consultas**: El serializer soporta batch queries para evitar el problema N+1 al obtener múltiples productos

4. **Camel Case**: Los serializers transforman los nombres de campos de snake_case (Python) a camelCase (JavaScript) para consistencia con el frontend

5. **Permisos**: Actualmente `permission_classes = [AllowAny]` - considerar cambiar a `[IsAuthenticated]` en producción
