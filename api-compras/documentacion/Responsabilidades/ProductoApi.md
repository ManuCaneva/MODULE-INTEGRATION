# productoApi

API REST para consulta de productos y categorías. Actúa como proxy entre el frontend y el servicio externo de Stock, con capacidad de operar en modo mock para desarrollo y testing.

---

## 📁 Estructura de archivos

### **`models.py`**
Define el modelo de datos para categorías:

#### **`Categoria`**
Modelo para clasificación de productos:
- `nombre`: Nombre único de la categoría (max 100 caracteres)
- `descripcion`: Descripción opcional de la categoría
- `activo`: Indicador booleano para habilitar/deshabilitar (default: True)
- `fecha_creacion`: Timestamp automático de creación

**Configuración del modelo**:
- `ordering`: Ordenado alfabéticamente por nombre
- `verbose_name`: "Categoría" / "Categorías" (configuración Django Admin)
- Restricción `unique=True` en campo `nombre`

**Nota importante**: Este modelo es para gestión interna de categorías. Los productos NO se persisten en base de datos local, solo se consultan desde Stock API o mock.

**Responsabilidad**: Gestión de categorías de productos para filtrado y organización. Provee clasificación estable independiente de cambios en Stock API.

---

### **`serializer.py`**
Serializer para transformación de datos:

#### **`CategoriaSerializer`**
Serializa el modelo Categoria para exposición en API:
- **Campos incluidos**: Todos los campos del modelo (`fields = '__all__'`)
- **Campos read-only**: `id`, `fecha_creacion` (no modificables por API)

**Responsabilidad**: Transformación entre objetos Categoria Django y JSON. Validación automática de datos según definición del modelo.

---

### **`views.py`**
ViewSets RESTful con lógica de negocio:

#### **`CategoriaViewSet`** (heredado de `viewsets.ModelViewSet`)
CRUD completo de categorías:

**Endpoints estándar**:
- `GET    /categorias/` - Listar categorías activas
- `POST   /categorias/` - Crear categoría
- `GET    /categorias/{id}/` - Detalle de categoría
- `PUT    /categorias/{id}/` - Actualizar categoría
- `PATCH  /categorias/{id}/` - Actualización parcial
- `DELETE /categorias/{id}/` - Eliminar categoría

**Filtrado**:
- `get_queryset()`: Filtra automáticamente solo categorías con `activo=True`
- Ordenado por nombre alfabéticamente

**Responsabilidad**: Gestión CRUD de categorías locales.

---

#### **`ProductoViewSet`** (heredado de `viewsets.ViewSet`)
Proxy inteligente hacia Stock API con fallback mock:

**Endpoints**:
- `list()` - `GET /api/product/` - Listar productos con paginación y filtros
- `retrieve()` - `GET /api/product/{id}/` - Detalle de producto específico

##### **Modo de operación dual**

**🔹 MODO MOCK** (`USE_MOCK_APIS=True` en settings):

**`list()`**: Listado desde datos locales
- **Fuente de datos**: Lista `MOCK_PRODUCTS` (90 productos hardcodeados en `views.py`)
- **Filtros soportados**:
  - `search` / `q`: Búsqueda en nombre y descripción (case-insensitive)
  - `categoria`: Filtra por nombre exacto de categoría
  - `marca`: Filtra por nombre exacto de marca
- **Paginación simulada**:
  - `page`: Número de página (default: 1)
  - `limit`: Productos por página (default: 12)
  - Calcula `total_pages` dinámicamente
- **Estructura de respuesta**:
  ```json
  {
    "data": [...],
    "pagination": {
      "page": 1,
      "per_page": 12,
      "total": 90,
      "total_pages": 8
    }
  }
  ```

**`retrieve(pk)`**: Detalle desde mock
- Busca en `MOCK_PRODUCTS` por campo `id`
- Devuelve 404 si no encuentra coincidencia
- Valida que `pk` sea entero válido

**Productos mock incluidos**: 90 productos distribuidos en:
- **Remeras**: 12 productos (IDs 1-5, 34-36, 51-52, 65-66, 79-80)
- **Pantalones**: 14 productos (IDs 6-10, 37-40, 53-54, 67-68)
- **Zapatillas**: 20 productos (IDs 11-15, 41-44, 55-57, 69-71, 81-90)
- **Abrigos**: 20 productos (IDs 16-20, 31-33, 49-50, 58-59, 72-74)
- **Accesorios**: 20 productos (IDs 21-25, 45-48, 60-64, 75-78)
- **Hogar/Oficina**: 4 productos (IDs 26-30)

**Marcas**: UrbanFit, ProSport, ClassicLine, DenimCo, StepUp, NorthWind, HomePlus, OfficePro

---

**🔹 MODO REAL** (`USE_MOCK_APIS=False` en settings):

**`list()`**: Consulta Stock API externa
- Instancia `StockClient` con `settings.STOCK_API_BASE_URL`
- Llama a `stock_client.listar_productos(page, limit, q, categoriaId)`
- **Parámetros enviados**:
  - `page`: Página solicitada (default: 1)
  - `limit`: Productos por página (default: 20)
  - `search` → `q`: Query de búsqueda
  - `categoria` → `categoriaId`: ID de categoría (convertido a int)
- **Manejo de errores**:
  - Errores de conexión: 502 Bad Gateway con `STOCK_SERVICE_UNAVAILABLE`
  - Otros errores: 500 Internal Server Error con `INTERNAL_ERROR`

**`retrieve(pk)`**: Detalle desde Stock API
- Llama a `stock_client.obtener_producto(int(pk))`
- Devuelve 404 si no existe
- Manejo de errores igual que `list()`

**Responsabilidad**: Proxy inteligente que abstrae la fuente de datos de productos. Permite desarrollo sin dependencias externas (mock) y producción con Stock API real. Maneja errores de conectividad gracefully.

---

### **`client.py`**
Cliente HTTP para consumir APIs de productos:

#### **`ProductoAPIClient`** (heredado de `BaseAPIClient`)
Cliente para consumir la propia API de productos (útil para testing o microservicios):

**Métodos disponibles**:
- `listar_productos(page, limit, search, categoria, marca)`: GET con filtros y paginación
- `obtener_producto(producto_id, parametros_extra)`: GET de producto específico

**Configuración**:
- URL base: `settings.PRODUCTOS_API_BASE_URL` (default: `http://localhost:8000/api/`)
- Timeout: 8.0s
- Max retries: 2
- Soporta autenticación con tokens y API keys

**Nota**: El método `listar_productos()` llama a `/api/product/` (no `/productos/`) según la configuración del router.

#### **`obtener_cliente_productos(**kwargs)`**
Factory function para instanciar ProductoAPIClient con configuración del proyecto:
```python
cliente = obtener_cliente_productos()
productos = cliente.listar_productos(page=1, limit=20, search="remera")
```

**Responsabilidad**: Abstracción de comunicación HTTP para consumir API de productos desde otros módulos o servicios. Facilita testing e integraciones.

---

### **`urls.py`**
Configuración de rutas HTTP:

```python
router = DefaultRouter()
router.register(r'product', ProductoViewSet, basename='producto')
```

**Endpoints generados automáticamente**:
- `GET    /api/product/` - Listar productos (con filtros y paginación)
- `GET    /api/product/{id}/` - Detalle de producto

**Nota**: La ruta base es `product` (singular) en lugar de `productos` (plural). Esto puede ser inconsistente con otros módulos que usan plural.

**Responsabilidad**: Enrutamiento de peticiones HTTP hacia ProductoViewSet usando Django REST Framework Router.

---

### **`apps.py`**
Configuración de la aplicación Django:

```python
class InicioConfig(AppConfig):
    name = 'apps.apis.productoApi'
    default_auto_field = 'django.db.models.BigAutoField'
```

**Responsabilidad**: Metadatos y configuración de la app para el registro en `INSTALLED_APPS`.

---

### **`admin.py`**
Configuración del panel de administración Django:

#### **`CategoriaAdmin`**
Registro del modelo Categoria en Django Admin:
- **`list_display`**: Muestra `id`, `nombre`, `activo`, `fecha_creacion` en listado
- **`list_filter`**: Filtros laterales por `activo` y `fecha_creacion`
- **`search_fields`**: Búsqueda por `nombre`
- **`list_editable`**: Permite editar campo `activo` directamente desde listado
- **`ordering`**: Ordenado alfabéticamente por `nombre`

**Responsabilidad**: Interfaz administrativa para gestionar categorías desde Django Admin (`/admin/productoApi/categoria/`).

---

### **`tests.py`**
Archivo para pruebas unitarias e integración (actualmente con imports básicos).

**Responsabilidad**: Testing de funcionalidad del módulo. Debe contener pruebas para:
- CRUD de categorías
- Listado de productos en modo mock
- Detalle de productos en modo mock
- Filtros y paginación
- Integración con Stock API en modo real
- Manejo de errores 404, 502, 500

---

## 🔗 Dependencias externas

### **Stock API** (módulo externo)
- **Endpoint**: Configurado en `settings.STOCK_API_BASE_URL`
- **Uso**: Fuente de datos de productos en modo real (`USE_MOCK_APIS=False`)
- **Métodos utilizados**:
  - `listar_productos(page, limit, q, categoriaId)`: Listado con filtros
  - `obtener_producto(producto_id)`: Detalle de producto

**Nota**: Este módulo NO persiste productos localmente, solo actúa como proxy.

---

## 🔧 Configuración requerida

En `settings.py`:

```python
# URLs de servicios externos
STOCK_API_BASE_URL = 'http://localhost:8001/api/'
PRODUCTOS_API_BASE_URL = 'http://localhost:8000/api/'

# Modo de operación
USE_MOCK_APIS = True  # False en producción con Stock API real

# Configuración de cliente HTTP
PRODUCTO_CLIENT_TIMEOUT = 8.0
PRODUCTO_CLIENT_MAX_RETRIES = 2
```

---

## 📊 Flujo de datos

### **Modo Mock (desarrollo)**:
```
Usuario → Frontend → GET /api/product/
    ↓
ProductoViewSet.list()
    ↓
Filtra MOCK_PRODUCTS (lista hardcodeada)
    ↓
Aplica filtros: search, categoria, marca
    ↓
Pagina resultados
    ↓
Response JSON con data + pagination
```

### **Modo Real (producción)**:
```
Usuario → Frontend → GET /api/product/
    ↓
ProductoViewSet.list()
    ↓
StockClient.listar_productos() → Stock API externa
    ↓
Maneja errores de conexión (502 Bad Gateway)
    ↓
Response con datos de Stock API
```

---

## 🧪 Testing

Para ejecutar las pruebas del módulo:

```powershell
python manage.py test apps.apis.productoApi
```

---

## 📝 Notas de implementación

1. **Sin persistencia de productos**: Los productos NO se guardan en base de datos local. Solo las categorías se persisten.

2. **Modo dual (mock/real)**:
   - Mock: Lista hardcodeada de 90 productos para desarrollo
   - Real: Proxy a Stock API externa para producción
   - Controlado por `settings.USE_MOCK_APIS`

3. **Rutas inconsistentes**: El router usa `/api/product/` (singular) mientras otros módulos usan plural (`/api/pedidos/`, `/api/shopcart/`). Considerar estandarizar.

4. **Paginación diferente por modo**:
   - Mock: `limit` default 12
   - Real: `limit` default 20

5. **Filtros limitados en mock**: Solo soporta búsqueda exacta en `categoria` y `marca`. La búsqueda por texto (`search`) es case-insensitive substring match.

6. **Imágenes mock**: Las rutas de imagen en `MOCK_PRODUCTS` apuntan a `/static/imagenes/mock/` - asegurar que existan o usar placeholders.

7. **Categorías vs productos**:
   - Categorías: CRUD completo en base de datos
   - Productos: Solo lectura, sin escritura (delegado a Stock API)

8. **Manejo de errores robusto**: Distingue entre errores de conexión (502) y errores internos (500) para facilitar debugging.

9. **Cliente HTTP autoconfigurable**: `ProductoAPIClient` puede consumir su propia API o cualquier otra compatible con el contrato.

10. **Datos mock extensos**: 90 productos distribuidos en 6 categorías con precios, stock, marcas e imágenes. Útil para demos y desarrollo frontend sin backend externo.

---

## 🔄 Migración de mock a real

Al cambiar `USE_MOCK_APIS` de `True` a `False`:

1. **Asegurar Stock API disponible**: Verificar que `STOCK_API_BASE_URL` sea accesible
2. **Revisar contrato de API**: Stock API debe devolver estructura compatible:
   ```json
   {
     "data": [...],
     "pagination": {...}
   }
   ```
3. **Mapear IDs de categorías**: Los filtros por `categoriaId` deben coincidir con IDs de Stock API
4. **Probar conectividad**: Ejecutar `python manage.py shell` y probar:
   ```python
   from utils.apiCliente.stock import StockClient
   client = StockClient()
   client.listar_productos(page=1, limit=10)
   ```
5. **Monitorear errores 502**: Implementar retry logic o circuit breakers si Stock API es inestable
