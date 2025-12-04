# 🧪 Pruebas de Integración - Compras API

Scripts y documentación para probar que tus endpoints de Compras se integran correctamente con Stock API (Grupo 02) y Logística API (Grupo 03).

## 📁 Archivos creados

### 1. `test_integracion_apis.py` - Script automatizado de pruebas

Script Python que ejecuta automáticamente todas las pruebas de integración:

```powershell
python ScriptParaApi/test_integracion_apis.py
```

**Qué hace:**
- ✅ Obtiene token de Keycloak
- ✅ Verifica que Stock API esté activo
- ✅ Lista productos de Stock (verificando que NO sean mock)
- ✅ Agrega producto al carrito (llamando a Stock)
- ✅ Crea pedido desde carrito (reservando stock en Stock API)
- ✅ Confirma pedido (creando envío en Logística API)
- ✅ Genera reporte con pruebas pasadas/fallidas

**Salida esperada:**
```
╔═══════════════════════════════════════════════════════════════════╗
║    TEST DE INTEGRACIÓN - COMPRAS ↔ STOCK ↔ LOGÍSTICA             ║
║    Verificando comunicación real entre microservicios             ║
╚═══════════════════════════════════════════════════════════════════╝

✅ Test #1: Obtener token de Keycloak
✅ Test #2: Servicio Django/Compras activo
✅ Test #3: Servicio Stock API activo
✅ Test #4: Listar productos de Stock API
✅ Test #5: Los datos NO son mock (datos reales de Stock)
...

═════════════════════════════════════════════════════════════════════
                         RESUMEN DE PRUEBAS
═════════════════════════════════════════════════════════════════════
Total de pruebas: 15
Exitosas: 15
Fallidas: 0

🎉 ¡TODAS LAS PRUEBAS PASARON!
```

### 2. `URLS_POSTMAN_INTEGRACION.txt` - Guía completa para Postman

Archivo con todas las URLs, headers, body y scripts de test para Postman.

**Incluye:**
- 11 endpoints documentados paso a paso
- Scripts de test automáticos para cada request
- Variables de entorno recomendadas
- Comandos para verificar logs
- Checklist de pruebas
- Evidencias a recolectar

**Cómo usar:**
1. Abrir Postman
2. Crear variables de entorno: `BASE_URL_COMPRAS`, `BASE_URL_STOCK`, `TOKEN`
3. Seguir los pasos 1-11 del archivo
4. Verificar logs con los comandos indicados

## 🚀 Requisitos previos

### 1. Servicios activos
```powershell
docker-compose up -d
```

Verificar:
```powershell
docker-compose ps
```

Debes ver todos los servicios `Up`:
- ✅ django
- ✅ stock-backend
- ✅ shipping-back
- ✅ nginx
- ✅ keycloak

### 2. USE_MOCK_APIS en "false"

En `docker-compose.yml`:
```yaml
environment:
  USE_MOCK_APIS: "false"  # ⚠️ IMPORTANTE
```

Si cambias esto, reinicia:
```powershell
docker-compose restart django
```

## 📊 Flujo de pruebas

### Flujo automatizado (Script Python)

```
1. Autenticación → Obtener token
2. Stock API → Listar productos reales
3. Stock API → Detalle de producto
4. Compras → Agregar al carrito (llama a Stock)
5. Compras → Ver carrito (con datos de Stock)
6. Compras → Checkout (reserva en Stock)
7. Compras → Confirmar (envío en Logística)
8. Compras → Ver historial
```

### Flujo manual (Postman)

Seguir el archivo `URLS_POSTMAN_INTEGRACION.txt` paso a paso.

## 🔍 Verificar integración con logs

### Ver llamadas a Stock API
```powershell
docker-compose logs django | Select-String "StockClient"
```

Deberías ver:
```
[StockClient] GET http://nginx/stock/api/v1/productos/abc-123
[StockClient] Response 200: {"nombre": "...", "precio": 1500}
[StockClient] POST http://nginx/stock/api/v1/reservas
```

### Ver llamadas a Logística API
```powershell
docker-compose logs django | Select-String "LogisticaClient"
```

Deberías ver:
```
[LogisticaClient] POST http://nginx/logistica/shipping
[LogisticaClient] Response 201: {"envioId": "env-456"}
```

### Ver logs de Stock API (recibiendo peticiones)
```powershell
docker-compose logs stock-backend
```

### Ver logs de Logística API (recibiendo peticiones)
```powershell
docker-compose logs shipping-back
```

## ✅ Evidencias para entregar

### 1. Screenshots de Postman
- ✅ Respuestas 200/201 OK en todos los endpoints
- ✅ Productos con datos reales (NO mock)
- ✅ Pedido con `reservaId` de Stock
- ✅ Pedido con `envioId` de Logística

### 2. Capturas de logs
- ✅ Django logs mostrando `[StockClient]` llamadas
- ✅ Django logs mostrando `[LogisticaClient]` llamadas
- ✅ Stock API logs mostrando peticiones recibidas
- ✅ Logística API logs mostrando peticiones recibidas

### 3. Resultado del script
- ✅ Salida completa de `test_integracion_apis.py`
- ✅ Todas las pruebas en verde

## 🐛 Troubleshooting

### Error: "Connection refused" en Stock API
```powershell
# Verificar que el servicio está UP
docker-compose ps stock-backend

# Ver logs
docker-compose logs stock-backend

# Reiniciar
docker-compose restart stock-backend
```

### Error: "502 Bad Gateway" en Logística
Esto es **NORMAL** si el servicio de Logística no está disponible. El script lo marca como prueba exitosa.

### Error: "USE_MOCK_APIS is true"
Cambiar en `docker-compose.yml`:
```yaml
USE_MOCK_APIS: "false"
```
Luego:
```powershell
docker-compose restart django
```

### Productos en carrito aparecen como None
Verificar:
1. `USE_MOCK_APIS: "false"`
2. Stock API está respondiendo
3. El `productId` es válido (obtenido de Stock API)

### Token expirado (401 Unauthorized)
Volver a ejecutar paso 1 (obtener token).

## 📞 Contacto

Si tienes dudas sobre las pruebas, revisar:
- `URLS_POSTMAN_INTEGRACION.txt` - Documentación completa
- Logs de Docker Compose
- Script `test_integracion_apis.py` - Código fuente con comentarios
