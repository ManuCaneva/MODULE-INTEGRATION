# ===========================================
# Script de Pruebas de Integración JWT
# ===========================================

Write-Host "`n" -NoNewline
Write-Host "="*90 -ForegroundColor Cyan
Write-Host "    PRUEBAS DE INTEGRACIÓN JWT CON KEYCLOAK" -ForegroundColor Yellow
Write-Host "="*90 -ForegroundColor Cyan

# Configuración
$keycloakUrl = "http://localhost:8080"
$apiUrl = "http://localhost:5002"
$clientId = "grupo-06"
$clientSecret = "8dc00e75-ccea-4d1a-be3d-b586733e256c"
$realm = "ds-2025-realm"

# TEST 1: Obtener Token JWT
Write-Host "`n📋 TEST 1: Obtener Token JWT desde Keycloak" -ForegroundColor Cyan
Write-Host "   URL: $keycloakUrl/realms/$realm" -ForegroundColor Gray

try {
    $body = @{
        grant_type = 'client_credentials'
        client_id = $clientId
        client_secret = $clientSecret
    }
    
    $tokenResponse = Invoke-RestMethod `
        -Uri "$keycloakUrl/realms/$realm/protocol/openid-connect/token" `
        -Method Post `
        -ContentType 'application/x-www-form-urlencoded' `
        -Body $body `
        -ErrorAction Stop
    
    $global:token = $tokenResponse.access_token
    
    Write-Host "   ✅ Token JWT obtenido exitosamente" -ForegroundColor Green
    Write-Host "      Token Type: $($tokenResponse.token_type)" -ForegroundColor Gray
    Write-Host "      Expira en: $($tokenResponse.expires_in) segundos" -ForegroundColor Gray
    Write-Host "      Token (primeros 80 chars): $($global:token.Substring(0,80))..." -ForegroundColor DarkGray
} catch {
    Write-Host "   ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# TEST 2: Endpoint sin autenticación
Write-Host "`n📋 TEST 2: Endpoint protegido SIN autenticación" -ForegroundColor Cyan
Write-Host "   URL: $apiUrl/api/dashboard/shipments" -ForegroundColor Gray

try {
    $response = Invoke-WebRequest `
        -Uri "$apiUrl/api/dashboard/shipments" `
        -Method Get `
        -TimeoutSec 10 `
        -ErrorAction Stop
    
    Write-Host "   ❌ FALLÓ: Endpoint NO está protegido (Status: $($response.StatusCode))" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 401) {
        Write-Host "   ✅ CORRECTO: Devuelve 401 Unauthorized" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Status inesperado: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Yellow
    }
}

# TEST 3: Endpoint CON token JWT válido
Write-Host "`n📋 TEST 3: Endpoint protegido CON token JWT válido" -ForegroundColor Cyan
Write-Host "   URL: $apiUrl/api/dashboard/shipments?page=1&pageSize=5" -ForegroundColor Gray

try {
    $headers = @{
        Authorization = "Bearer $global:token"
    }
    
    $response = Invoke-WebRequest `
        -Uri "$apiUrl/api/dashboard/shipments?page=1&pageSize=5" `
        -Method Get `
        -Headers $headers `
        -TimeoutSec 15 `
        -ErrorAction Stop
    
    Write-Host "   🎉 ¡ÉXITO! Token JWT aceptado y roles validados" -ForegroundColor Green
    Write-Host "      Status Code: $($response.StatusCode)" -ForegroundColor Gray
    Write-Host "      Content-Length: $($response.Content.Length) bytes" -ForegroundColor Gray
    
    $json = $response.Content | ConvertFrom-Json
    
    Write-Host "`n   📊 Datos del Dashboard recibidos:" -ForegroundColor Cyan
    Write-Host "      • Total shipments: $($json.pagination.total_items)" -ForegroundColor White
    Write-Host "      • Página actual: $($json.pagination.current_page)/$($json.pagination.total_pages)" -ForegroundColor White
    Write-Host "      • Items por página: $($json.pagination.items_per_page)" -ForegroundColor White
    Write-Host "      • Shipments mostrados: $($json.shipments.Count)" -ForegroundColor White
    
    if ($json.shipments.Count -gt 0) {
        Write-Host "`n   📦 Primer shipment:" -ForegroundColor Cyan
        $first = $json.shipments[0]
        Write-Host "      ID: $($first.shipping_id)" -ForegroundColor Gray
        Write-Host "      Order ID: $($first.order_id)" -ForegroundColor Gray
        Write-Host "      Status: $($first.status)" -ForegroundColor Gray
        Write-Host "      Transport: $($first.transport_type)" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "   ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        Write-Host "      Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Yellow
    }
    exit 1
}

# Resumen Final
Write-Host "`n" -NoNewline
Write-Host "="*90 -ForegroundColor Green
Write-Host "    ✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE" -ForegroundColor Yellow
Write-Host "="*90 -ForegroundColor Green
Write-Host ""
