# Contratos mínimos: Stock y Logística

Este documento define contratos mínimos (payloads y respuestas) para integrar Compras con los servicios de Stock y Logística. Son propuestas pensadas para un primer flujo síncrono/temporal.

---

## 1) Contrato mínimo - Stock

### Reservar stock (POST)
- URL: `/api/stock/reservas/` (ejemplo)
- Método: `POST`
- Encabezados: `Content-Type: application/json`

Request JSON (body):
{
  "idCompra": "<string-idempotency>",
  "usuarioId": 123,
  "products": [
    { "productId": 10, "quantity": 2 },
    { "productId": 35, "quantity": 1 }
  ]
}

Response 201 (reservado):
{
  "id": 9876,
  "reservationId": 9876,          // campo alternativo
  "idCompra": "<same>",
  "status": "reserved",
  "products": [
    { "productId": 10, "quantity": 2 },
    { "productId": 35, "quantity": 1 }
  ],
  "meta": { "reserved_at": "2025-11-13T12:00:00Z" }
}

Response 409 (insuficiente stock):
HTTP 409
{
  "error": "Insufficient stock",
  "detail": {
    "productId": 10,
    "available": 1,
    "requested": 2
  }
}

Notes / recomendaciones:
- `idCompra` debe ser usado como idempotency key: reintentos con el mismo `idCompra` no deben crear reservas duplicadas.
- Respuesta debe incluir un `id`/`reservationId` único para referenciarla.
- Incluir un TTL (por ejemplo 1 hora) para la reserva y permitir `liberar` con motivo.

### Liberar reserva (POST)
- URL: `/api/stock/reservas/{reservationId}/liberar/`
- Método: `POST`
- Body:
{ "usuarioId": 123, "motivo": "Compensación por fallo logística" }
- Respuesta 200: `{ "ok": true, "reservationId": 9876 }`

### Consultar reserva (GET)
- URL: `/api/stock/reservas/{reservationId}/`
- Respuesta 200 (ejemplo):
{
  "id": 9876,
  "status": "reserved",             // or cancelled, expired
  "products": [...],
  "expires_at": "2025-11-13T13:00:00Z"
}

---

## 2) Contrato mínimo - Logística

### Listar métodos de envío (GET)
- URL: `/api/logistica/methods/`
- Respuesta 200:
[
  { "id": "domicilio", "name": "Envío a domicilio", "cost": 3500, "eta": "3-5 días" },
  { "id": "retiro_sucursal", "name": "Retiro en sucursal", "cost": 0, "eta": "Disponible hoy" }
]

### Calcular costo (POST) - opcional
- URL: `/api/logistica/calculate/`
- Body:
{
  "deliveryAddress": { "ciudad": "X", "codigo_postal": "1234" },
  "products": [{ "productId": 10, "quantity": 2 }],
  "transport_type": "domicilio"
}
- Response 200: `{ "cost": 3500, "eta": "3-5 días" }`

### Crear envío / Booking (POST)
- URL: `/api/logistica/shipments/`
- Método: `POST`
- Request JSON (body):
{
  "order_id": 555,                    // id local del pedido
  "user_id": 123,
  "idCompra": "<idempotency-client>",
  "delivery_address": {
    "nombre_receptor": "Juan Perez",
    "calle": "Av Siempreviva 123",
    "ciudad": "Rosario",
    "provincia": "Santa Fe",
    "codigo_postal": "2000",
    "pais": "Argentina",
    "telefono": "3411234567",
    "informacion_adicional": "Puerta 2"
  },
  "transport_type": "domicilio",
  "products": [{ "productId": 10, "quantity": 2 }],
  "meta": { "peso_total_kg": 2.5 }
}

Response 201 (exitoso):
{
  "id": 4242,
  "trackingId": "TRK-4242",
  "status": "created",
  "eta": "2025-11-18",
  "quoted_cost": 3500
}

Response 400/502 (error):
{
  "error": "Invalid address",
  "detail": "Falta campo calle"
}

Notes / recomendaciones:
- Mantener `idCompra` como idempotency key para evitar duplicados si el cliente reintenta.
- Responder con `trackingId` o `id` y `status`.
- En producción preferible: crear la reserva/logística de forma asíncrona y confirmar vía webhooks cuando estén listas.

---

## Ejemplo de flujo (resumen)
1. Cliente POST `/api/stock/reservas/` con `idCompra` + productos → obtiene `reservationId`.
2. Cliente POST `/api/logistica/shipments/` con `order_id`, `delivery_address`, `products`, `idCompra` → obtiene `trackingId`.
3. Si logística falla, cliente POST `/api/stock/reservas/{reservationId}/liberar/`.
4. Cuando todo ok, marcar `Pedido` como confirmado con `referencia_reserva_stock` y `referencia_envio`.

---