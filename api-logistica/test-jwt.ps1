# --- CONFIGURACION ---
$tokenUrl = "http://localhost:8080/realms/ds-2025-realm/protocol/openid-connect/token"
$apiUrl = "http://localhost:5002/api/dashboard/shipments"
$clientId = "grupo-06"
$clientSecret = "8dc00e75-ccea-4d1a-be3d-b586733e256c"

# --- PASO 1: PEDIR TOKEN ---
Write-Host "1. Solicitando Token a Keycloak..." -ForegroundColor Cyan
$body = @{
    grant_type = 'client_credentials'
    client_id = $clientId
    client_secret = $clientSecret
}

try {
    $response = Invoke-RestMethod -Uri $tokenUrl -Method Post -Body $body
    $token = $response.access_token
    Write-Host "   [OK] Token recibido." -ForegroundColor Green
} catch {
    Write-Host "   [ERROR] No se pudo obtener token: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# --- PASO 2: PROBAR API CON TOKEN ---
Write-Host "2. Probando API (Logística)..." -ForegroundColor Cyan
$headers = @{
    Authorization = "Bearer $token"
}

try {
    # Hacemos la llamada GET simple
    Invoke-WebRequest -Uri $apiUrl -Method Get -Headers $headers -TimeoutSec 5
    Write-Host "   [OK] ¡ÉXITO! La API aceptó el token (Status 200)." -ForegroundColor Green
} catch {
    $ex = $_.Exception
    Write-Host "   [FAIL] Falló la API: $($ex.Message)" -ForegroundColor Red
    if ($ex.Response) {
        Write-Host "   Status Code: $($ex.Response.StatusCode.value__)" -ForegroundColor Yellow
    }
}