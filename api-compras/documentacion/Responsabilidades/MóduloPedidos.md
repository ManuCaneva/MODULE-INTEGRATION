# pedidos

Módulo frontend de gestión de pedidos del usuario. Proporciona interfaces web para el ciclo completo de compra: desde el checkout hasta la confirmación de pago, historial de órdenes y seguimiento de estados.

---

## 🎯 Responsabilidad General

Este módulo actúa como **capa de presentación** para el flujo de pedidos del e-commerce. Se encarga de:

- **Checkout**: Formulario para completar datos de envío y seleccionar método de entrega
- **Confirmación**: Orquestación del proceso de confirmación integrando Stock y Logística
- **Historial**: Visualización de pedidos previos del usuario con filtros por estado
- **Feedback de pago**: Páginas de confirmación exitosa o fallida post-transacción
- **Administración**: Panel interno para gestionar pedidos con datos de prueba en desarrollo

**Arquitectura**: Importa modelos desde `pedidoApi` (fuente única de verdad) y consume endpoints REST internos para mantener desacoplamiento entre frontend y backend.

---

## 📁 Estructura de archivos

### **`models.py`**
Importa modelos de `pedidoApi` sin duplicar definiciones:

```python
from apps.apis.pedidoApi.models import Pedido, DetallePedido, DireccionEnvio
```

**Responsabilidad**: Reutilizar modelos existentes como fuente única de verdad.

---

### **`views.py`**
Controladores para las diferentes pantallas del flujo de pedidos:

#### **Vistas principales**

- **`checkout_view()`**: Formulario de checkout con opciones de envío (domicilio, sucursal, exprés)
- **`mis_pedidos()`**: Historial de pedidos consumiendo API REST (`/api/shopcart/history`)
- **`listar_pedidos()`**: Panel administrativo con filtros por estado y datos de prueba (seeding con `?seed=1`)
- **`pago_exitoso()` / `pago_fallido()`**: Páginas de feedback post-transacción

#### **API Endpoint**

- **`api_checkout_confirm()`**: Endpoint crítico que orquesta el flujo completo de confirmación:
  1. Validación de datos (dirección, productos)
  2. Creación de pedido en estado BORRADOR
  3. Reserva de stock en Stock API
  4. Creación de envío en Logística API
  5. Confirmación del pedido o compensación si falla

**Características clave**:
- Manejo de transacciones con compensación automática (libera stock si falla envío)
- Logging extensivo para debugging
- Códigos de error HTTP semánticos (400, 401, 409, 500, 502)

#### **Funciones auxiliares**

- **`_ensure_demo_user()`**: Crea usuario demo para testing
- **`_seed_demo_pedidos()`**: Genera 3 pedidos de prueba con productos mockeados

**Responsabilidad**: Orquestar el flujo de pedidos integrando Stock y Logística APIs, renderizar pantallas de usuario y proveer datos de prueba en desarrollo.

---

### **`urls.py`**
Enrutamiento del módulo bajo namespace `pedidos`:

- `/` → Historial de pedidos del usuario
- `/admin/` → Panel administrativo con filtros por estado
- `/checkout/` → Formulario de checkout
- `/api/checkout/confirm/` → Endpoint API de confirmación
- `/pago/exitoso/` → Página de confirmación exitosa
- `/pago/fallido/` → Página de error de pago

**Responsabilidad**: Definir rutas bajo `/pedidos/*` para frontend y API endpoint.

---

### **`templates/`**
Templates HTML para las diferentes pantallas:

- **`checkout.html`**: Formulario de checkout con opciones de envío
- **`pedidos/listar_pedidos.html`**: Panel administrativo con tabla filtrable
- **`pedidos/mis_pedidos.html`**: Historial de pedidos del usuario
- **`pedidos/pago_exitoso.html`**: Confirmación de pago exitoso
- **`pedidos/pago_fallido.html`**: Notificación de pago fallido

**Responsabilidad**: Presentación visual del flujo de pedidos.

---

### **`apps.py`**
Configuración de la aplicación Django con nombre `apps.modulos.pedidos`.

**Responsabilidad**: Registro de la app en `INSTALLED_APPS`.

---

### **`admin.py`** y **`tests.py`**
Archivos estándar de Django (actualmente vacíos o con imports básicos).

**Responsabilidad**: Configuración de Django Admin y pruebas unitarias pendientes de implementar.

---

## 🔗 Dependencias principales

- **pedidoApi**: Importa modelos `Pedido`, `DetallePedido`, `DireccionEnvio`
- **Stock API**: Reserva y liberación de stock de productos
- **Logística API**: Creación de envíos y tracking
- **API REST interna**: Consume `/api/shopcart/history` para historial

---

## 🔧 Configuración básica

En `settings.py`:

```python
BASE_URL = 'http://localhost:8000'
STOCK_API_BASE_URL = 'http://localhost:8001/api/'
LOGISTICA_API_BASE_URL = 'http://localhost:8002/api/'
```

En `Main/urls.py`:

```python
path('pedidos/', include('apps.modulos.pedidos.urls')),
```

---

## 📊 Flujos principales

### **Checkout completo**
```
Usuario → Formulario checkout → POST /api/checkout/confirm/
  → Crear dirección + pedido
  → Reservar stock
  → Crear envío
  → Confirmar pedido
  → Redirect /pago/exitoso/
```

### **Compensación en caso de fallo**
```
Falla creación de envío
  → Liberar automáticamente reserva de stock
  → Retornar error 502
  → Redirect /pago/fallido/
```

---

## 📝 Notas importantes

1. **Modelos compartidos**: No duplica modelos, importa desde `pedidoApi`
2. **Compensación automática**: Si falla envío, libera stock automáticamente (patrón Saga)
3. **Seeding de datos**: Solo en DEBUG con `?seed=1`
4. **API híbrida**: Incluye endpoint REST (`api_checkout_confirm`) en módulo frontend
5. **Costos hardcodeados**: Opciones de envío con precios fijos ($5.000, $8.500)

---

## 🚀 Mejoras futuras sugeridas

- Mover `api_checkout_confirm` a `pedidoApi` para mejor separación
- Obtener costos de envío dinámicamente desde Logística API
- Implementar cancelación de pedidos con liberación de recursos
- Agregar notificaciones por email en cambios de estado
- Integrar pasarelas de pago (MercadoPago, Stripe)
- Sistema de tracking de envío en tiempo real

