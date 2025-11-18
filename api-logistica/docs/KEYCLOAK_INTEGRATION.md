# Guía de Integración JWT con Keycloak

## ✅ Configuración Completada

La API ahora está integrada con Keycloak para autenticación JWT Bearer. Se han realizado los siguientes cambios:

### 1. Paquete Instalado
- `Microsoft.AspNetCore.Authentication.JwtBearer` (v8.0.11)

### 2. Configuración en `Program.cs`
- Autenticación JWT Bearer configurada con Keycloak como Authority
- Middleware de autenticación y autorización agregados al pipeline

### 3. Configuración en `appsettings.json`
```json
"Authentication": {
  "Keycloak": {
    "Authority": "http://localhost:8080/realms/ds-2025-realm",
    "Audience": "account"
  }
},
"Keycloak": {
  "ClientId": "grupo-06",
  "ClientSecret": "404249de-18ba-403c-b45c-d82c446e2a2a",
  "TokenEndpoint": "http://localhost:8080/realms/ds-2025-realm/protocol/openid-connect/token"
}
```

### 4. Controllers Actualizados
- `DashboardController`: Ahora usa `[Authorize(Roles = "logistica-be")]`
- Otros controllers permanecen públicos (sin autenticación)

## 🚀 Cómo Usar

### 1. Levantar Keycloak
```bash
cd src/keycloak
docker compose up -d
```

### 2. Obtener Token JWT

```bash
curl --location 'http://localhost:8080/realms/ds-2025-realm/protocol/openid-connect/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'client_id=grupo-06' \
--data-urlencode 'client_secret=404249de-18ba-403c-b45c-d82c446e2a2a'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI...",
  "expires_in": 300,
  "token_type": "Bearer"
}
```

### 3. Usar el Token en Peticiones

```bash
curl --location 'http://localhost:5000/api/dashboard/shipments' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI...'
```

## 🔐 Información del Cliente

- **Cliente ID**: `grupo-06`
- **Client Secret**: `404249de-18ba-403c-b45c-d82c446e2a2a`
- **Rol Asignado**: `logistica-be`
- **Scopes Disponibles**:
  - usuarios:read
  - productos:read
  - envios:read, envios:write
  - reservas:read, reservas:write
  - stock:read, stock:write

## 📋 Endpoints Protegidos

| Endpoint | Método | Autenticación | Rol Requerido |
|----------|--------|---------------|---------------|
| `/api/dashboard/shipments` | GET | ✅ Requerida | `logistica-be` |
| `/shipping` | POST | ❌ Público | - |
| `/shipping/cost` | POST | ❌ Público | - |
| `/api/shipping` | GET | ❌ Público | - |
| `/locality` | GET | ❌ Público | - |

## 🛠️ Próximos Pasos

### Para Proteger Más Endpoints
Agrega el atributo `[Authorize]` o `[Authorize(Roles = "rol-name")]` a los controllers que necesites proteger:

```csharp
[ApiController]
[Route("shipping")]
[Authorize] // Requiere autenticación (cualquier token válido)
public class ShippingCreateController : ControllerBase
{
    // ...
}
```

O con rol específico:
```csharp
[Authorize(Roles = "logistica-be")] // Solo rol específico
```

### Para Frontend (Svelte)
El frontend debe:
1. Obtener el token desde Keycloak usando el flujo Client Credentials
2. Almacenar el token (sessionStorage/localStorage)
3. Enviarlo en cada petición:
```javascript
const response = await fetch('http://localhost:5000/api/dashboard/shipments', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

### Verificar JWKS
Los tokens se validan automáticamente contra: 
`http://localhost:8080/realms/ds-2025-realm/protocol/openid-connect/certs`

## 🐛 Debug

Si hay problemas con los tokens, verás logs en consola:
- "Authentication failed: {mensaje}"
- "Token validated successfully"

Para más detalle, revisa los logs de la aplicación .NET.

## 📚 Documentación Adicional

- [Keycloak README](../keycloak/README.md)
- [OpenAPI Spec](../../docs/openapi1.1.yaml)
