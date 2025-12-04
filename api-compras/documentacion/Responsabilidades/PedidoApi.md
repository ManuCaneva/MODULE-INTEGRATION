# pedidoApi

API REST para gestión del ciclo completo de pedidos. Orquesta la integración entre el carrito de compras, las reservas de stock y la logística de envíos.

---

## 📁 Estructura de archivos

### **`models.py`**
Define los modelos de datos para pedidos y envíos:

#### **`DireccionEnvio`**
Dirección de entrega asociada a un pedido:
- `usuario`: Relación opcional con User (puede ser anónimo)
- `nombre_receptor`: Nombre de quien recibe
- `calle`, `ciudad`, `provincia`, `codigo_postal`, `pais`: Componentes de dirección
- `telefono`: Contacto del receptor
- `informacion_adicional`: Detalles extras (piso, depto, referencias)
- `generar_datos_logistica()`: Transforma el modelo a formato esperado por Logística API

#### **`Pedido`**
Pedido del usuario con seguimiento de estado:
- **Estados**: `BORRADOR`, `PENDIENTE`, `CONFIRMADO`, `CANCELADO`
- `usuario`: Relación opcional con User (soporta compras sin autenticación)
- `direccion_envio`: OneToOne con DireccionEnvio
- `estado`: Estado actual del pedido (default: PENDIENTE)
- `tipo_transporte`: Tipo de envío (`domicilio`, `retiro_sucursal`, `demo_tracking`)
- `total`: Monto total del pedido (calculado automáticamente)
- `referencia_envio`: ID del envío en Logística API
- `referencia_reserva_stock`: ID de reserva en Stock API
- `confirmado_en`: Timestamp de confirmación
- **Métodos**:
  - `recalcular_total(guardar=True)`: Suma los precios de todos los detalles
  - `marcar_confirmado(referencia_envio, referencia_reserva_stock)`: Cambia estado a CONFIRMADO y guarda referencias externas

#### **`DetallePedido`**
Representa cada producto dentro de un pedido:
- `pedido`: Relación ForeignKey con Pedido
- `producto_id`: ID del producto (referencia externa a Stock)
- `nombre_producto`: Nombre del producto (desnormalizado para historial)
- `cantidad`: Cantidad ordenada (mínimo 1)
- `precio_unitario`: Precio en el momento de la compra
- `precio_total` (property): Calcula `precio_unitario * cantidad`

**Responsabilidad**: Persistencia del pedido y su historial. Desacopla la información de productos para mantener registro histórico aunque cambien en Stock.

---

### **`serializer.py`**
Serializers para transformación de datos entre Django ORM y JSON:

#### **`DireccionEnvioSerializer`**
Serializa direcciones de envío:
- Expone todos los campos de dirección
- `id` es read-only

#### **`DetallePedidoSerializer`**
Serializa ítems individuales del pedido:
- `precio_total`: Campo calculado con `get_precio_total()`
- `id` y `precio_total` son read-only

#### **`PedidoSerializer`**
Serializer principal con lógica de negocio compleja:
- **Campos anidados**:
  - `direccion_envio`: DireccionEnvioSerializer (requerido en creación)
  - `detalles`: Lista de DetallePedidoSerializer (requerido en creación)
- **Campos calculados**:
  - `estado_display`: Nombre legible del estado (`get_estado_display()`)
  - `total`: Calculado automáticamente sumando detalles
- **Métodos**:
  - `_obtener_usuario()`: Obtiene usuario autenticado del request context
  - `create()`: Crea pedido con transacción atómica (direccion + pedido + detalles)
  - `update()`: Actualiza pedido validando que no esté confirmado
  - `to_representation()`: Enriquece respuesta con detalles y dirección completa

**Validaciones automáticas**:
- Impide edición de pedidos confirmados
- Requiere dirección de envío y al menos un producto
- Calcula total automáticamente

**Responsabilidad**: Transformación y validación de datos. Asegura integridad referencial y cálculos correctos.

---

### **`views.py`**
ViewSet RESTful que orquesta toda la lógica de negocio:

#### **`PedidoViewSet`** (heredado de `viewsets.ModelViewSet`)

**Endpoints estándar:**
- `list()` - `GET /api/pedidos/`: Lista pedidos del usuario
- `retrieve()` - `GET /api/pedidos/{id}/`: Detalle de un pedido
- `create()` - `POST /api/pedidos/`: Crea pedido (heredado de ModelViewSet)
- `update()` - `PUT/PATCH /api/pedidos/{id}/`: Actualiza pedido
- `destroy()` - `DELETE /api/pedidos/{id}/`: Elimina pedido (solo si no está confirmado)

**Actions personalizados:**

##### **`confirmar()`** - `POST /api/pedidos/{id}/confirmar/`
Confirma un pedido ejecutando el flujo completo de integración:

**Validaciones**:
- Pedido no puede estar ya confirmado
- Pedido no puede estar cancelado
- Debe tener productos asociados
- Requiere tipo de transporte

**Flujo de ejecución**:
1. Recalcula total del pedido si es 0.00
2. Crea envío en Logística API con `create_shipment()`
3. Reserva stock en Stock API con `reservar_stock()`
4. Marca pedido como confirmado guardando ambas referencias
5. Si algún servicio falla, devuelve 502 Bad Gateway con detalles

##### **`cancelar()`** - `DELETE /api/pedidos/{id}/cancelar/`
Cancela un pedido y libera recursos externos:

**Validaciones**:
- No se puede cancelar un pedido ya cancelado
- No se puede cancelar un pedido confirmado (envío en tránsito)

**Flujo de ejecución**:
1. Si existe `referencia_reserva_stock`, llama a `cancelar_reserva()` en Stock API
2. Si existe `referencia_envio`, llama a `cancel_shipment()` en Logística API
3. Marca pedido como CANCELADO usando transacción atómica
4. Si fallan los servicios externos, devuelve 502 con detalles

##### **`history()`** - `GET /api/shopcart/history`
Lista historial de pedidos del usuario autenticado:
- Usa `get_queryset()` que ya filtra por usuario
- Devuelve todos los pedidos del usuario con todos sus detalles

##### **`history_detail()`** - `GET /api/shopcart/history/{id}`
Obtiene un pedido específico del historial:
- Usa `get_object()` para validar permisos y existencia
- Devuelve 404 si el pedido no existe o no pertenece al usuario

##### **`crear_desde_carrito()`** - `POST /api/shopcart/checkout`
Crea un pedido desde un carrito mock (sin autenticación requerida):

**Validaciones**:
- Requiere `items` en payload (lista de productos)
- Requiere `nombre_receptor`
- Si tipo_transporte NO es `retiro_sucursal` ni `demo_tracking`, valida dirección completa (`calle`, `ciudad`, `cp`)
- Si es retiro en sucursal, dirección es opcional

**Flujo de ejecución**:
1. Crea DireccionEnvio con datos del request
2. Crea Pedido en estado PENDIENTE sin usuario
3. Itera sobre items mock y crea DetallePedido por cada uno
4. Calcula total sumando `cantidad * precio` de cada item
5. **Agrega costo de envío al total**
6. Devuelve `pedido_id` y objeto completo serializado

##### **`crear_tracking()`** - `POST /api/pedidos/{id}/tracking/`
Vincula un pedido con un envío en Logística creando un tracking:

**Validaciones**:
- Pedido no puede tener tracking previo
- Debe tener productos asociados
- Requiere tipo de transporte

**Flujo de ejecución**:
1. Llama a `create_tracking()` en Logística API
2. Extrae `tracking_id` de la respuesta (soporta múltiples nombres de campo)
3. Guarda `tracking_id` en `referencia_envio` del pedido
4. Devuelve objeto tracking y pedido_id

##### **`obtener_tracking()`** - `GET /api/pedidos/{id}/tracking/`
Obtiene el estado del envío asociado al pedido:

**Validaciones**:
- Pedido debe tener `referencia_envio` asociada

**Flujo de ejecución**:
1. Llama a `get_tracking(tracking_id)` en Logística API
2. Fallback: si falla, intenta `get_shipment(tracking_id)`
3. Devuelve datos del tracking y pedido_id

**Permisos**:
- Actualmente `permission_classes = [AllowAny]` para desarrollo
- En producción cambiar a `[IsAuthenticated]` excepto `crear_desde_carrito`

**Responsabilidad**: Controlador HTTP que orquesta operaciones complejas entre múltiples servicios (Stock, Logística, Carrito). Maneja validaciones, transacciones y rollback ante errores.

---

### **`client.py`**
Cliente HTTP para comunicación con APIs externas:

#### **`PedidoAPIClient`** (heredado de `BaseAPIClient`)
Cliente para consumir la propia API de pedidos (útil para testing o integraciones):

**Métodos disponibles**:
- `obtener_pedido(pedido_id)`: GET de pedido específico
- `crear_pedido(direccion_envio, detalles, tipo_transporte)`: POST para crear pedido
- `confirmar_pedido(pedido_id, tipo_transporte)`: POST para confirmar
- `cancelar_pedido(pedido_id)`: DELETE para cancelar
- `history(**params)`: GET del historial de pedidos
- `history_detail(pedido_id)`: GET de pedido específico del historial
- `crear_tracking(pedido_id, tipo_transporte)`: POST para crear tracking
- `obtener_tracking(pedido_id)`: GET del tracking asociado

**Configuración**:
- URL base: `settings.PEDIDOS_API_BASE_URL` (default: `http://localhost:8000/api/`)
- Timeout: 8.0s
- Max retries: 2
- Soporta autenticación con tokens y API keys

#### **Factory functions**

##### **`obtener_cliente_pedidos(**kwargs)`**
Instancia PedidoAPIClient con configuración del proyecto:
```python
cliente = obtener_cliente_pedidos()
pedido = cliente.crear_pedido(
    direccion_envio={...},
    detalles=[...],
    tipo_transporte="domicilio"
)
```

##### **`obtener_cliente_logistica()`**
Instancia LogisticsClient para integración con Logística:
```python
cliente = obtener_cliente_logistica()
envio = cliente.create_shipment(
    order_id=123,
    user_id=45,
    delivery_address={...},
    transport_type="domicilio",
    products=[...]
)
```

##### **`obtener_cliente_stock()`**
Instancia StockClient para integración con Stock:
```python
cliente = obtener_cliente_stock()
reserva = cliente.reservar_stock(
    idCompra="123",
    usuarioId=45,
    productos=[{"idProducto": 1, "cantidad": 2}]
)
```

**Responsabilidad**: Abstracción de comunicación HTTP. Desacopla las vistas de los detalles de las APIs externas. Facilita testing mediante inyección de dependencias.

---

### **`urls.py`**
Configuración de rutas REST usando Django REST Framework Router:

```python
router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')
```

**Endpoints generados automáticamente**:
- `GET    /api/pedidos/` - Listar pedidos
- `POST   /api/pedidos/` - Crear pedido
- `GET    /api/pedidos/{id}/` - Detalle de pedido
- `PUT    /api/pedidos/{id}/` - Actualizar pedido
- `PATCH  /api/pedidos/{id}/` - Actualización parcial
- `DELETE /api/pedidos/{id}/` - Eliminar pedido
- `POST   /api/pedidos/{id}/confirmar/` - Confirmar pedido
- `DELETE /api/pedidos/{id}/cancelar/` - Cancelar pedido
- `GET    /api/pedidos/history/` - Historial de pedidos
- `GET    /api/pedidos/{id}/history-detail/` - Detalle del historial
- `POST   /api/pedidos/{id}/tracking/` - Crear tracking
- `GET    /api/pedidos/{id}/tracking/` - Obtener tracking

**Responsabilidad**: Enrutamiento de peticiones HTTP hacia el ViewSet usando convenciones REST.

---

### **`frontend_urls.py`**
Rutas alternativas según especificación OpenAPI del frontend:

**Propósito**: Mantener compatibilidad con el contrato OpenAPI definido para el cliente web.

**Endpoints mapeados**:
- `GET    /api/shopcart/history` → `PedidoViewSet.history()`
- `GET    /api/shopcart/history/{id}` → `PedidoViewSet.history_detail()`
- `DELETE /api/shopcart/history/{id}` → `PedidoViewSet.cancelar()`
- `POST   /api/shopcart/checkout` → `PedidoViewSet.crear_desde_carrito()`

**Nota**: Estas URLs coexisten con las de `urls.py`. El frontend usa `/api/shopcart/*` mientras que otras integraciones usan `/api/pedidos/*`.

**Responsabilidad**: Proporcionar rutas alternativas para mantener contratos OpenAPI específicos del frontend.

---

### **`apps.py`**
Configuración de la aplicación Django:

```python
class pedidoApiConfig(AppConfig):
    name = 'apps.apis.pedidoApi'
    default_auto_field = 'django.db.models.BigAutoField'
```

**Responsabilidad**: Metadatos y configuración de la app para el registro en `INSTALLED_APPS`.

---

### **`admin.py`**
Registro de modelos en el panel de administración Django (actualmente vacío).

**Responsabilidad**: Configuración del Django Admin para gestionar pedidos desde el panel web administrativo.

---

### **`tests.py`**
Archivo para pruebas unitarias e integración (actualmente con imports básicos).


## 🔗 Dependencias externas

### **Stock API** (módulo externo)
- **Endpoint**: Configurado en `settings.STOCK_API_BASE_URL`
- **Uso**: Reservar y liberar stock de productos
- **Métodos utilizados**:
  - `reservar_stock(idCompra, usuarioId, productos)`: Reserva productos para un pedido
  - `cancelar_reserva(idReserva, idCompra)`: Libera stock al cancelar pedido
  - `obtener_producto(producto_id)`: Consulta información de producto

### **Logística API** (módulo externo)
- **Endpoint**: Configurado en `settings.LOGISTICS_API_BASE_URL`
- **Uso**: Crear envíos y trackings
- **Métodos utilizados**:
  - `create_shipment(order_id, user_id, delivery_address, transport_type, products)`: Crea un envío
  - `cancel_shipment(shipping_id, order_id)`: Cancela un envío
  - `create_tracking(...)`: Crea tracking de seguimiento
  - `get_tracking(tracking_id)`: Consulta estado del envío
  - `get_shipment(shipping_id)`: Fallback para obtener datos del envío

### **Carrito API** (módulo interno)
- **Uso**: Obtener productos del carrito para checkout
- **Métodos utilizados**:
  - `obtener_items(usuario_id)`: Obtiene ítems del carrito para crear pedido

---

## 🔧 Configuración requerida

En `settings.py`:

```python
# URLs de servicios externos
STOCK_API_BASE_URL = 'http://localhost:8001/api/'
LOGISTICS_API_BASE_URL = 'http://localhost:8002/api/'
PEDIDOS_API_BASE_URL = 'http://localhost:8000/api/'

# Configuración de cliente HTTP
PEDIDO_CLIENT_TIMEOUT = 8.0
PEDIDO_CLIENT_MAX_RETRIES = 2
```

---

## 📊 Flujo de datos

### **Creación de pedido:**
```
Usuario → Frontend → POST /api/shopcart/checkout
    ↓
PedidoViewSet.crear_desde_carrito()
    ↓
DireccionEnvio.objects.create()
Pedido.objects.create(estado=PENDIENTE)
DetallePedido.objects.create() × N
    ↓
Response con pedido_id
```

### **Confirmación de pedido:**
```
Usuario → Frontend → POST /api/pedidos/{id}/confirmar/
    ↓
PedidoViewSet.confirmar()
    ↓
LogisticsClient.create_shipment() → Logística API
    ↓
StockClient.reservar_stock() → Stock API
    ↓
Pedido.marcar_confirmado(referencia_envio, referencia_reserva_stock)
    ↓
Response con pedido confirmado
```

### **Cancelación de pedido:**
```
Usuario → Frontend → DELETE /api/shopcart/history/{id}
    ↓
PedidoViewSet.cancelar()
    ↓
StockClient.cancelar_reserva() → Stock API
    ↓
LogisticsClient.cancel_shipment() → Logística API
    ↓
Pedido.estado = CANCELADO
    ↓
Response con mensaje de éxito
```

---

## 🧪 Testing

Para ejecutar las pruebas del módulo:

```powershell
python manage.py test apps.apis.pedidoApi
```

---

## 📝 Notas de implementación

1. **Transacciones atómicas**: Todas las operaciones de escritura usan `@transaction.atomic` para garantizar consistencia

2. **Desnormalización**: Los detalles del pedido guardan `nombre_producto` y `precio_unitario` para mantener historial aunque cambien en Stock

3. **Pedidos anónimos**: El campo `usuario` es nullable para soportar compras sin autenticación (modo guest checkout)

4. **Manejo de errores**: Los errores de APIs externas devuelven 502 Bad Gateway con detalles del error para facilitar debugging

5. **Tipos de transporte**: Soporta `domicilio`, `retiro_sucursal`, `demo_tracking`. Para retiro en sucursal, la dirección es opcional

6. **Referencia externa dual**: Cada pedido confirmado guarda:
   - `referencia_envio`: ID del envío en Logística
   - `referencia_reserva_stock`: ID de reserva en Stock
   
7. **Costo de envío**: Se calcula y agrega al total en el checkout desde el frontend

8. **Estados del pedido**:
   - `BORRADOR`: Creado pero sin finalizar (no usado actualmente)
   - `PENDIENTE`: Creado pero sin confirmar (estado inicial)
   - `CONFIRMADO`: Stock reservado y envío creado
   - `CANCELADO`: Cancelado manualmente, stock y envío liberados

9. **Permisos**: Actualmente `AllowAny` para desarrollo. En producción:
   - `crear_desde_carrito`: Mantener AllowAny (guest checkout)
   - Resto de endpoints: Cambiar a `IsAuthenticated`

10. **Rutas duales**: El módulo expone dos conjuntos de URLs:
    - `/api/pedidos/*`: API REST estándar
    - `/api/shopcart/*`: Alias para compatibilidad con frontend
