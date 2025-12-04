#  URLs de Peticiones - Grupo COMPRAS → LOGÍSTICA y STOCK

**Destinatario:** Grupos de Logística y Stock  
**Propósito:** Configurar sus servidores con las URLs exactas donde Compras estará haciendo peticiones  
**Fecha:** 20 de Noviembre, 2025

---

## 📍 URL Base Configurada

### Desde Código (Default)
```python
STOCK_API_BASE_URL = "http://localhost:8000"
LOGISTICA_API_BASE_URL = "http://localhost:8000"
```

### Desde Variables de Entorno (.env)
```
STOCK_API_BASE_URL=http://localhost/stock/
LOGISTICA_API_BASE_URL=http://localhost/logistica/
```

---

## 🎯 PETICIONES QUE HACE COMPRAS A STOCK

### ✅ Endpoint: Listar Productos

**Método:** `GET`  
**URL:** `{STOCK_API_BASE_URL}/api/mock/stock/productos`  
**URL Completa (Default):** `http://localhost:8000/api/mock/stock/productos`  
**URL Completa (.env):** `http://localhost/stock/api/mock/stock/productos`

**Cliente:** `StockClient`  
**Método:** `listar_productos(page=1, limit=20, q=None, categoriaId=None)`

**Parámetros Query:**
```json
{
  "page": 1,
  "limit": 20,
  "q": "busqueda_opcional",
  "categoriaId": 1
}
```

**Respuesta Esperada:**
```json
{
  "results": [
    {
      "id": 1,
      "nombre": "Producto",
      "precio": 100,
      "stock": 10
    }
  ],
  "count": 1,
  "next": null,
  "previous": null
}
```

**Usado en:** 
- `apps/modulos/inicio/views.py` - Listar productos disponibles
- `apps/apis/productoApi/views.py` - API de productos del carrito

---

### ✅ Endpoint: Obtener Producto Específico

**Método:** `GET`  
**URL:** `{STOCK_API_BASE_URL}/api/mock/stock/productos/{productoId}`  
**URL Completa (Default):** `http://localhost:8000/api/mock/stock/productos/1`  
**URL Completa (.env):** `http://localhost/stock/api/mock/stock/productos/1`

**Cliente:** `StockClient`  
**Método:** `obtener_producto(productoId: int)`

**Parámetros:** Ninguno

**Respuesta Esperada:**
```json
{
  "id": 1,
  "nombre": "Producto",
  "descripcion": "Descripción",
  "precio": 100,
  "stock": 10,
  "categoriaId": 1
}
```

**Usado en:**
- `apps/modulos/pedidos/views.py` - Obtener detalles del producto en checkout

---

### ✅ Endpoint: Reservar Stock

**Método:** `POST`  
**URL:** `{STOCK_API_BASE_URL}/api/mock/stock/stock/reservar`  
**URL Completa (Default):** `http://localhost:8000/api/mock/stock/stock/reservar`  
**URL Completa (.env):** `http://localhost/stock/api/mock/stock/stock/reservar`

**Cliente:** `StockClient`  
**Método:** `reservar_stock(idCompra: str, usuarioId: int, productos: list)`

**Body:**
```json
{
  "idCompra": "ORD-20251120-001",
  "usuarioId": 1,
  "productos": [
    {
      "idProducto": 1,
      "cantidad": 5
    },
    {
      "idProducto": 2,
      "cantidad": 3
    }
  ]
}
```

**Respuesta Esperada:**
```json
{
  "idReserva": 123,
  "idCompra": "ORD-20251120-001",
  "estado": "reservado",
  "productos": [...],
  "fecha": "2025-11-20T10:30:00Z"
}
```

**Usado en:**
- `apps/modulos/pedidos/views.py` - Confirmar pedido (antes de crear envío)

---

### ✅ Endpoint: Listar Reservas

**Método:** `GET`  
**URL:** `{STOCK_API_BASE_URL}/api/mock/stock/reservas`  
**URL Completa (Default):** `http://localhost:8000/api/mock/stock/reservas`  
**URL Completa (.env):** `http://localhost/stock/api/mock/stock/reservas`

**Cliente:** `StockClient`  
**Método:** `listar_reservas(usuarioId: int, page: int = 1, limit: int = 20, estado: Optional[str] = None)`

**Parámetros Query:**
```json
{
  "usuarioId": 1,
  "page": 1,
  "limit": 20,
  "estado": "reservado"
}
```

**Respuesta Esperada:**
```json
{
  "results": [
    {
      "idReserva": 123,
      "idCompra": "ORD-001",
      "estado": "reservado",
      "fecha": "2025-11-20T10:30:00Z"
    }
  ],
  "count": 1,
  "next": null
}
```

---

### ✅ Endpoint: Obtener Reserva Específica

**Método:** `GET`  
**URL:** `{STOCK_API_BASE_URL}/api/mock/stock/reservas/{idReserva}`  
**URL Completa (Default):** `http://localhost:8000/api/mock/stock/reservas/123`  
**URL Completa (.env):** `http://localhost/stock/api/mock/stock/reservas/123`

**Cliente:** `StockClient`  
**Método:** `obtener_reserva(idReserva: int, usuarioId: int)`

**Parámetros Query:**
```json
{
  "usuarioId": 1
}
```

**Respuesta Esperada:**
```json
{
  "idReserva": 123,
  "idCompra": "ORD-001",
  "usuarioId": 1,
  "estado": "reservado",
  "productos": [...]
}
```

---

### ✅ Endpoint: Listar Categorías

**Método:** `GET`  
**URL:** `{STOCK_API_BASE_URL}/api/mock/stock/categorias`  
**URL Completa (Default):** `http://localhost:8000/api/mock/stock/categorias`  
**URL Completa (.env):** `http://localhost/stock/api/mock/stock/categorias`

**Cliente:** `StockClient`  
**Método:** `listar_categorias()`

**Parámetros:** Ninguno

**Respuesta Esperada:**
```json
[
  {
    "id": 1,
    "nombre": "Electrónica",
    "descripcion": "Productos electrónicos"
  }
]
```

---

### ✅ Endpoint: Obtener Categoría Específica

**Método:** `GET`  
**URL:** `{STOCK_API_BASE_URL}/api/mock/stock/categorias/{categoriaId}`  
**URL Completa (Default):** `http://localhost:8000/api/mock/stock/categorias/1`  
**URL Completa (.env):** `http://localhost/stock/api/mock/stock/categorias/1`

**Cliente:** `StockClient`  
**Método:** `obtener_categoria(categoriaId: int)`

**Respuesta Esperada:**
```json
{
  "id": 1,
  "nombre": "Electrónica",
  "descripcion": "Productos electrónicos"
}
```

---

### ✅ Endpoint: Liberar Stock (Cancelación)

**Método:** `POST`  
**URL:** `{STOCK_API_BASE_URL}/api/mock/stock/stock/liberar`  
**URL Completa (Default):** `http://localhost:8000/api/mock/stock/stock/liberar`  
**URL Completa (.env):** `http://localhost/stock/api/mock/stock/stock/liberar`

**Cliente:** `StockClient`  
**Método:** `liberar_stock(idReserva: int, usuarioId: int, motivo: str)`

**Body:**
```json
{
  "idReserva": 123,
  "usuarioId": 1,
  "motivo": "Pedido cancelado por usuario"
}
```

**Respuesta Esperada:**
```json
{
  "idReserva": 123,
  "estado": "liberado",
  "mensaje": "Stock liberado exitosamente"
}
```

**Usado en:**
- `apps/modulos/pedidos/views.py` - Cancelar pedido

---

## 🚚 PETICIONES QUE HACE COMPRAS A LOGÍSTICA

### ✅ Endpoint: Obtener Métodos de Transporte

**Método:** `GET`  
**URL:** `{LOGISTICA_API_BASE_URL}/shipping/transport-methods`  
**URL Completa (Default):** `http://localhost:8000/shipping/transport-methods`  
**URL Completa (.env):** `http://localhost/logistica/shipping/transport-methods`

**Cliente:** `LogisticsClient`  
**Método:** `get_transport_methods()`

**Parámetros:** Ninguno

**Respuesta Esperada:**
```json
[
  {
    "id": "air",
    "nombre": "Aéreo",
    "descripcion": "Envío por aire",
    "dias_entrega": 2,
    "costo_base": 50
  },
  {
    "id": "road",
    "nombre": "Terrestre",
    "descripcion": "Envío por tierra",
    "dias_entrega": 7,
    "costo_base": 20
  }
]
```

**Usado en:**
- `apps/modulos/pedidos/views.py` - Mostrar opciones de envío al usuario

---

### ✅ Endpoint: Calcular Costo de Envío

**Método:** `POST`  
**URL:** `{LOGISTICA_API_BASE_URL}/shipping/cost`  
**URL Completa (Default):** `http://localhost:8000/shipping/cost`  
**URL Completa (.env):** `http://localhost/logistica/shipping/cost`

**Cliente:** `LogisticsClient`  
**Método:** `calculate_shipping_cost(delivery_address, products, transport_type=None)`

**Body:**
```json
{
  "delivery_address": {
    "street": "Calle Principal 123",
    "city": "Buenos Aires",
    "state": "BA",
    "postal_code": "1428",
    "country": "Argentina"
  },
  "products": [
    {
      "id": 1,
      "quantity": 5
    }
  ],
  "transport_type": "air"
}
```

**Respuesta Esperada:**
```json
{
  "costo_envio": 100.50,
  "costo_base": 50,
  "costo_distancia": 30.50,
  "impuestos": 20,
  "dias_entrega": 2,
  "metodo_transporte": "air"
}
```

**Usado en:**
- `apps/modulos/pedidos/views.py` - Mostrar costo de envío en checkout

---

### ✅ Endpoint: Crear Envío (Shipping)

**Método:** `POST`  
**URL:** `{LOGISTICA_API_BASE_URL}/shipping`  
**URL Completa (Default):** `http://localhost:8000/shipping`  
**URL Completa (.env):** `http://localhost/logistica/shipping`

**Cliente:** `LogisticsClient`  
**Método:** `create_shipment(order_id, user_id, delivery_address, transport_type, products)`

**Body:**
```json
{
  "order_id": 1,
  "user_id": 1,
  "delivery_address": {
    "street": "Calle Principal 123",
    "city": "Buenos Aires",
    "state": "BA",
    "postal_code": "1428",
    "country": "Argentina"
  },
  "transport_type": "air",
  "products": [
    {
      "id": 1,
      "quantity": 5
    }
  ]
}
```

**Respuesta Esperada:**
```json
{
  "shipping_id": 456,
  "order_id": 1,
  "status": "pendiente",
  "tracking_number": "TRACK-20251120-001",
  "fecha_creacion": "2025-11-20T10:30:00Z",
  "fecha_entrega_estimada": "2025-11-22T00:00:00Z"
}
```

**Usado en:**
- `apps/modulos/pedidos/views.py` - Confirmar pedido y crear envío

---

### ✅ Endpoint: Listar Envíos

**Método:** `GET`  
**URL:** `{LOGISTICA_API_BASE_URL}/shipping`  
**URL Completa (Default):** `http://localhost:8000/shipping`  
**URL Completa (.env):** `http://localhost/logistica/shipping`

**Cliente:** `LogisticsClient`  
**Método:** `list_shipments(user_id=None, status=None, from_date=None, to_date=None, page=1, limit=20)`

**Parámetros Query:**
```json
{
  "user_id": 1,
  "status": "pendiente",
  "from_date": "2025-11-01",
  "to_date": "2025-11-30",
  "page": 1,
  "limit": 20
}
```

**Respuesta Esperada:**
```json
{
  "results": [
    {
      "shipping_id": 456,
      "order_id": 1,
      "status": "en_transito",
      "tracking_number": "TRACK-001"
    }
  ],
  "count": 1,
  "next": null
}
```

---

### ✅ Endpoint: Obtener Envío Específico

**Método:** `GET`  
**URL:** `{LOGISTICA_API_BASE_URL}/shipping/{shipping_id}`  
**URL Completa (Default):** `http://localhost:8000/shipping/456`  
**URL Completa (.env):** `http://localhost/logistica/shipping/456`

**Cliente:** `LogisticsClient`  
**Método:** `get_shipment(shipping_id: int)`

**Parámetros:** Ninguno

**Respuesta Esperada:**
```json
{
  "shipping_id": 456,
  "order_id": 1,
  "user_id": 1,
  "status": "en_transito",
  "tracking_number": "TRACK-20251120-001",
  "delivery_address": {...},
  "fecha_creacion": "2025-11-20T10:30:00Z",
  "fecha_entrega_estimada": "2025-11-22T00:00:00Z",
  "eventos_tracking": [...]
}
```

**Usado en:**
- `apps/modulos/pedidos/views.py` - Obtener detalles del envío

---

### ✅ Endpoint: Crear Tracking

**Método:** `POST`  
**URL:** `{LOGISTICA_API_BASE_URL}/logistics/tracking`  
**URL Completa (Default):** `http://localhost:8000/logistics/tracking`  
**URL Completa (.env):** `http://localhost/logistica/logistics/tracking`

**Cliente:** `LogisticsClient`  
**Método:** `create_tracking(order_id, user_id, delivery_address, transport_type, products)`

**Body:**
```json
{
  "order_id": 1,
  "user_id": 1,
  "delivery_address": {
    "street": "Calle Principal 123",
    "city": "Buenos Aires",
    "state": "BA",
    "postal_code": "1428",
    "country": "Argentina"
  },
  "transport_type": "air",
  "products": [
    {
      "id": 1,
      "quantity": 5
    }
  ]
}
```

**Respuesta Esperada:**
```json
{
  "tracking_id": 789,
  "order_id": 1,
  "status": "en_preparacion",
  "numero_seguimiento": "TRACK-20251120-001"
}
```

**Usado en:**
- `apps/apis/pedidoApi/views.py` - Crear tracking para un pedido

---

### ✅ Endpoint: Obtener Tracking

**Método:** `GET`  
**URL:** `{LOGISTICA_API_BASE_URL}/logistics/tracking/{tracking_id}`  
**URL Completa (Default):** `http://localhost:8000/logistics/tracking/789`  
**URL Completa (.env):** `http://localhost/logistica/logistics/tracking/789`

**Cliente:** `LogisticsClient`  
**Método:** `get_tracking(tracking_id: int)`

**Parámetros:** Ninguno

**Respuesta Esperada:**
```json
{
  "tracking_id": 789,
  "order_id": 1,
  "user_id": 1,
  "numero_seguimiento": "TRACK-20251120-001",
  "estado": "entregado",
  "eventos": [
    {
      "fecha": "2025-11-20T10:30:00Z",
      "estado": "en_preparacion",
      "ubicacion": "Almacén Central"
    },
    {
      "fecha": "2025-11-21T14:00:00Z",
      "estado": "en_transito",
      "ubicacion": "Centro de distribución"
    }
  ]
}
```

**Usado en:**
- `apps/apis/pedidoApi/views.py` - Obtener estado de tracking

---

### ✅ Endpoint: Cancelar Envío

**Método:** `POST`  
**URL:** `{LOGISTICA_API_BASE_URL}/shipping/{shipping_id}/cancel`  
**URL Completa (Default):** `http://localhost:8000/shipping/456/cancel`  
**URL Completa (.env):** `http://localhost/logistica/shipping/456/cancel`

**Cliente:** `LogisticsClient`  
**Método:** `cancel_shipment(shipping_id: int)`

**Body:**
```json
{}
```

**Respuesta Esperada:**
```json
{
  "shipping_id": 456,
  "status": "cancelado",
  "mensaje": "Envío cancelado exitosamente"
}
```

**Usado en:**
- `apps/modulos/pedidos/views.py` - Cancelar envío cuando se cancela pedido

---

## 📊 Tabla Resumen de URLs

### STOCK API

| Operación | Método | Ruta | URL Completa |
|-----------|--------|------|--------------|
| Listar Productos | GET | `/api/mock/stock/productos` | `http://localhost:8000/api/mock/stock/productos` |
| Obtener Producto | GET | `/api/mock/stock/productos/{id}` | `http://localhost:8000/api/mock/stock/productos/1` |
| Listar Categorías | GET | `/api/mock/stock/categorias` | `http://localhost:8000/api/mock/stock/categorias` |
| Obtener Categoría | GET | `/api/mock/stock/categorias/{id}` | `http://localhost:8000/api/mock/stock/categorias/1` |
| **Reservar Stock** | **POST** | **/api/mock/stock/stock/reservar** | **http://localhost:8000/api/mock/stock/stock/reservar** |
| Listar Reservas | GET | `/api/mock/stock/reservas` | `http://localhost:8000/api/mock/stock/reservas` |
| Obtener Reserva | GET | `/api/mock/stock/reservas/{id}` | `http://localhost:8000/api/mock/stock/reservas/123` |
| Liberar Stock | POST | `/api/mock/stock/stock/liberar` | `http://localhost:8000/api/mock/stock/stock/liberar` |

### LOGÍSTICA API

| Operación | Método | Ruta | URL Completa |
|-----------|--------|------|--------------|
| Métodos Transporte | GET | `/shipping/transport-methods` | `http://localhost:8000/shipping/transport-methods` |
| Calcular Costo | POST | `/shipping/cost` | `http://localhost:8000/shipping/cost` |
| **Crear Envío** | **POST** | **/shipping** | **http://localhost:8000/shipping** |
| Listar Envíos | GET | `/shipping` | `http://localhost:8000/shipping` |
| Obtener Envío | GET | `/shipping/{id}` | `http://localhost:8000/shipping/456` |
| Cancelar Envío | POST | `/shipping/{id}/cancel` | `http://localhost:8000/shipping/456/cancel` |
| Crear Tracking | POST | `/logistics/tracking` | `http://localhost:8000/logistics/tracking` |
| Obtener Tracking | GET | `/logistics/tracking/{id}` | `http://localhost:8000/logistics/tracking/789` |

---

## 🔐 Autenticación

**Encabezados requeridos:**
```http
Accept: application/json
Content-Type: application/json
Authorization: Bearer {token}  # Si es requerido
```

**Token obtenido de:** `http://localhost:8080/realms/ds-2025-realm/protocol/openid-connect/token`

---

## ⚙️ Configuración Recomendada

### Para Stock
```env
STOCK_API_BASE_URL=http://localhost:8000
# o en producción/docker:
STOCK_API_BASE_URL=http://stock-service:8000
```

### Para Logística
```env
LOGISTICA_API_BASE_URL=http://localhost:8000
# o en producción/docker:
LOGISTICA_API_BASE_URL=http://logistica-service:8000
```

---

## Flujo Completo de una Compra

```
1. GET  {STOCK_API_BASE_URL}/api/mock/stock/productos
   → Listar productos disponibles para el usuario

2. GET  {STOCK_API_BASE_URL}/api/mock/stock/productos/{id}
   → Obtener detalles de un producto específico

3. GET  {LOGISTICA_API_BASE_URL}/shipping/transport-methods
   → Mostrar opciones de envío

4. POST {LOGISTICA_API_BASE_URL}/shipping/cost
   → Calcular costo de envío según dirección

5. POST {STOCK_API_BASE_URL}/api/mock/stock/stock/reservar
   → Reservar stock de los productos

6. POST {LOGISTICA_API_BASE_URL}/shipping
   → Crear envío/shipping

7. POST {LOGISTICA_API_BASE_URL}/logistics/tracking
   → Crear tracking para seguimiento

8. GET  {LOGISTICA_API_BASE_URL}/logistics/tracking/{id}
   → Usuario consulta estado del seguimiento
```

