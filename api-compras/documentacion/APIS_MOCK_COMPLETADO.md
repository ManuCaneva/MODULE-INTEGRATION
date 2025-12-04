# 🎉 APIs Mock - Implementación Completada

## ✅ Estado: LISTO PARA USAR

Las APIs mock de Stock y Logística han sido implementadas y están funcionando correctamente.

## 🚀 Servidor Activo

```
✅ Servidor corriendo en: http://127.0.0.1:8000/
⚠️  [DEV] Usando APIs MOCK locales para desarrollo
```

## 📡 Endpoints Disponibles

### Stock API Mock - Base: `/api/mock/stock/`

Con el router de DRF, los endpoints disponibles son:

| Endpoint | Descripción |
|----------|-------------|
| `GET /api/mock/stock/productos/` | Listar productos |
| `GET /api/mock/stock/categorias/` | Listar categorías |
| `GET /api/mock/stock/reservas/` | Listar reservas |
| `POST /api/mock/stock/stock/reservar/` | Reservar stock |
| `POST /api/mock/stock/stock/liberar/` | Liberar stock |

### Logística API Mock - Base: `/api/mock/logistica/`

| Endpoint | Descripción |
|----------|-------------|
| `GET /api/mock/logistica/shipping/transport-methods/` | Métodos de transporte |
| `POST /api/mock/logistica/shipping/cost/` | Calcular costo |
| `POST /api/mock/logistica/shipping/` | Crear envío |
| `GET /api/mock/logistica/shipping/` | Listar envíos |

## 🧪 Probar las APIs

### 1. Abrir en el navegador

```
http://127.0.0.1:8000/api/mock/stock/
http://127.0.0.1:8000/api/mock/logistica/
```

DRF mostrará una interfaz visual para probar los endpoints.

### 2. Con cURL

**Listar productos:**
```bash
curl http://127.0.0.1:8000/api/mock/stock/productos/
```

**Reservar stock:**
```bash
curl -X POST http://127.0.0.1:8000/api/mock/stock/stock/reservar/ ^
  -H "Content-Type: application/json" ^
  -d "{\"idCompra\": \"ORD-2025-001\", \"usuarioId\": 123, \"productos\": [{\"idProducto\": 1, \"cantidad\": 2}]}"
```

**Calcular costo de envío:**
```bash
curl -X POST http://127.0.0.1:8000/api/mock/logistica/shipping/cost/ ^
  -H "Content-Type: application/json" ^
  -d "{\"delivery_address\": {\"street\": \"Av. Corrientes 1234\", \"city\": \"Buenos Aires\", \"state\": \"CABA\", \"postal_code\": \"C1043\", \"country\": \"Argentina\"}, \"products\": [{\"id\": 1, \"quantity\": 2}], \"transport_type\": \"road\"}"
```

### 3. Con Python (Usando los clientes existentes)

```python
from utils.apiCliente.stock import StockClient
from utils.apiCliente.logistica import LogisticsClient
from Main.settings import STOCK_API_BASE_URL, LOGISTICS_API_BASE_URL

# Clientes apuntando a APIs mock
stock_client = StockClient(base_url=STOCK_API_BASE_URL)
logistics_client = LogisticsClient(base_url=LOGISTICS_API_BASE_URL)

# Listar productos
productos = stock_client.listar_productos(page=1, limit=10)
print(f"✅ Productos: {len(productos['data'])} encontrados")

# Reservar stock
reserva = stock_client.reservar_stock(
    idCompra="TEST-001",
    usuarioId=123,
    productos=[{"idProducto": 1, "cantidad": 2}]
)
print(f"✅ Reserva creada: {reserva['idReserva']}")

# Calcular costo de envío
costo = logistics_client.calculate_shipping_cost(
    delivery_address={
        "street": "Av. Corrientes 1234",
        "city": "Buenos Aires", 
        "state": "CABA",
        "postal_code": "C1043",
        "country": "Argentina"
    },
    products=[{"id": 1, "quantity": 2}],
    transport_type="road"
)
print(f"✅ Costo de envío: ${costo['estimated_cost']}")
```

## 💾 Datos de Prueba Cargados

### ✅ Stock API
- **4 Categorías:** Electrónica, Ropa, Hogar, Deportes
- **15 Productos:** Laptops, smartphones, ropa, electrodomésticos, etc.
- Stock variable: algunos productos con stock alto, otros con stock bajo o agotado

### ✅ Logística API
- **4 Métodos de Transporte:**
  - `air` - Aéreo (2 días, $45 base)
  - `road` - Terrestre (5 días, $15 base)
  - `sea` - Marítimo (20 días, $10 base)
  - `rail` - Ferroviario (7 días, $12 base)

## 🎨 Django Admin

Puedes gestionar los datos desde el panel de administración:

```
URL: http://127.0.0.1:8000/admin/
```

Si no tienes un superusuario, créalo:
```bash
python manage.py createsuperuser
```

### Modelos disponibles en Admin:
- **Stock API:** Categorías, Productos, Reservas
- **Logística API:** Métodos de Transporte, Envíos

## 🔄 Switch Desarrollo/Producción

En `Main/settings.py` (línea ~38):

```python
# ✅ ACTUALMENTE: Modo Desarrollo (APIs Mock)
USE_MOCK_APIS = True

# Para cambiar a APIs reales en producción:
USE_MOCK_APIS = False
```

Cuando cambies a `False`, asegúrate de configurar las URLs reales:
```python
STOCK_API_BASE_URL = os.environ.get("STOCK_API_BASE_URL", "https://api-stock-real.com")
LOGISTICS_API_BASE_URL = os.environ.get("LOGISTICS_API_BASE_URL", "https://api-logistica-real.com")
```

## 📊 Resumen de Implementación

| Componente | Estado | Archivos |
|------------|--------|----------|
| Modelos Stock | ✅ | `apps/apis/stockApi/models.py` |
| Views Stock | ✅ | `apps/apis/stockApi/views.py` |
| Serializers Stock | ✅ | `apps/apis/stockApi/serializers.py` |
| URLs Stock | ✅ | `apps/apis/stockApi/urls.py` |
| Admin Stock | ✅ | `apps/apis/stockApi/admin.py` |
| Modelos Logística | ✅ | `apps/apis/logisticaApi/models.py` |
| Views Logística | ✅ | `apps/apis/logisticaApi/views.py` |
| Serializers Logística | ✅ | `apps/apis/logisticaApi/serializers.py` |
| URLs Logística | ✅ | `apps/apis/logisticaApi/urls.py` |
| Admin Logística | ✅ | `apps/apis/logisticaApi/admin.py` |
| Fixtures | ✅ | 15 productos, 4 métodos de transporte |
| Migraciones | ✅ | Aplicadas correctamente |
| Configuración | ✅ | `settings.py`, `urls.py` |
| Documentación | ✅ | Este archivo + planificación |

## 🎯 Próximos Pasos Sugeridos

1. **Probar flujo completo:**
   - Listar productos
   - Reservar stock
   - Calcular costo de envío
   - Crear envío
   - Cancelar envío

2. **Integrar con tu módulo de pedidos:**
   - Usar `StockClient` para reservar productos al crear un pedido
   - Usar `LogisticsClient` para crear envío después de confirmar pago

3. **Testing:**
   - Crear tests unitarios para las APIs mock
   - Probar con diferentes escenarios (stock agotado, errores, etc.)

4. **Mejoras opcionales:**
   - Agregar más productos de prueba
   - Implementar endpoint para simular cambio de estado de envío
   - Agregar validaciones adicionales

## 📚 Documentación Completa

- **Planificación:** `documentacion/apis-internas-planificacion.md`
- **README APIs:** `apps/apis/README_APIS_MOCK.md`
- **Este documento:** Guía de inicio rápido

## 🐛 Troubleshooting

### Si el servidor no arranca:
```bash
python manage.py runserver
```

### Si faltan datos:
```bash
python manage.py loaddata apps/apis/stockApi/fixtures/productos_iniciales.json
python manage.py loaddata apps/apis/logisticaApi/fixtures/metodos_transporte.json
```

### Si hay errores de migración:
```bash
python manage.py migrate
```

## ✨ ¡Todo Listo!

Las APIs mock están funcionando y listas para usar. Puedes empezar a desarrollar y probar tu sistema sin depender de servicios externos.

**¡A programar con lluvia! ☔🚀**

---

**Fecha de implementación:** 16 de octubre de 2025  
**Branch:** api  
**Estado:** ✅ Completado y funcional
