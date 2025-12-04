using ComprasAPI.Models.DTOs;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Net.Http.Headers;
using System.Text.Json;

namespace ComprasAPI.Services
{
    public class StockService : IStockService
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<StockService> _logger;
        private readonly IConfiguration _configuration;

        private string _cachedToken;
        private DateTime _tokenExpiry;

        public StockService(HttpClient httpClient, ILogger<StockService> logger, IConfiguration configuration)
        {
            _httpClient = httpClient;
            _logger = logger;
            _configuration = configuration;
        }

        /*
        public async Task<bool> CancelarReservaAsync(int idReserva, int usuarioId)
        {
            try
            {
                _logger.LogInformation($"Cancelando reserva {idReserva}...");
                var httpRequest = await CreateAuthenticatedRequest(HttpMethod.Delete, $"/reservas/{idReserva}");
                var response = await _httpClient.SendAsync(httpRequest);

                if (response.IsSuccessStatusCode)
                {
                    _logger.LogInformation($"✅ Reserva {idReserva} cancelada exitosamente");
                    return true;
                }
                else
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    _logger.LogError($"❌ Error cancelando reserva {idReserva}: {response.StatusCode} - {errorContent}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"💥 Error cancelando reserva {idReserva}");
                return false;
            }
        }

        */

        public async Task<bool> CancelarReservaAsync(int idReserva, string motivo = "Rollback por falla en checkout")
        {
            try
            {
                _logger.LogInformation($"Cancelando reserva {idReserva}...");

                // ✅ SOLUCIÓN: Agregar el campo "motivo" que requiere Stock API
                var cancelRequest = new { motivo = motivo };

                var httpRequest = await CreateAuthenticatedRequest(HttpMethod.Delete, $"reservas/{idReserva}", cancelRequest);
                var response = await _httpClient.SendAsync(httpRequest);

                if (response.IsSuccessStatusCode)
                {
                    _logger.LogInformation($"✅ Reserva {idReserva} cancelada exitosamente");
                    return true;
                }
                else
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    _logger.LogError($"❌ Error cancelando reserva {idReserva}: {response.StatusCode} - {errorContent}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"💥 Error cancelando reserva {idReserva}");
                return false;
            }
        }

        public async Task<ReservaOutput> CrearReservaAsync(ReservaInput reserva)
        {
            try
            {
                _logger.LogInformation("🔄 Creando reserva en Stock API...");

                // CORRECCIÓN: Usar Productos (no Items)
                _logger.LogInformation($"Reserva para usuario {reserva.UsuarioId} con {reserva.Productos?.Count} productos");

                var httpRequest = await CreateAuthenticatedRequest(HttpMethod.Post, "reservas", reserva);
                var response = await _httpClient.SendAsync(httpRequest);

                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    _logger.LogInformation($"✅ Respuesta de Stock API: {responseContent}");

                    var reservaOutput = JsonSerializer.Deserialize<ReservaOutput>(responseContent, new JsonSerializerOptions
                    {
                        PropertyNameCaseInsensitive = true
                    });

                    // CORRECCIÓN: Usar IdReserva (no ReservaId)
                    _logger.LogInformation($"✅ Reserva creada exitosamente: {reservaOutput.IdReserva}");
                    return reservaOutput;
                }
                else
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    _logger.LogError($"❌ Error creando reserva: {response.StatusCode} - {errorContent}");
                    throw new Exception($"Error creando reserva: {response.StatusCode} - {errorContent}");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "💥 Error creando reserva en Stock API");
                throw;
            }
        }

        public async Task<ProductoStock> GetProductoAsync(int productoId)
        {
            try
            {
                _logger.LogInformation($"Obteniendo producto {productoId} desde Stock API...");

                var httpRequest = await CreateAuthenticatedRequest(HttpMethod.Get, $"productos/{productoId}");
                var response = await _httpClient.SendAsync(httpRequest);

                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    var producto = JsonSerializer.Deserialize<ProductoStock>(responseContent, new JsonSerializerOptions
                    {
                        PropertyNameCaseInsensitive = true
                    });

                    // CORRECCIÓN: Usar StockDisponible (no Stock)
                    _logger.LogInformation($"Producto {productoId} obtenido: {producto.Nombre} - Stock: {producto.StockDisponible}");
                    return producto;
                }
                else
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    throw new Exception($"Error obteniendo producto: {response.StatusCode} - {errorContent}");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error obteniendo producto {productoId}");
                throw;
            }
        }

        private async Task<HttpRequestMessage> CreateAuthenticatedRequest(HttpMethod method, string endpoint, object content = null)
        {
            var token = await GetAccessTokenAsync();
            var baseUrl = _configuration["ExternalApis:Stock:BaseUrl"] ?? "http://localhost:3000/";
            
            // Ensure baseUrl ends with /
            if (!baseUrl.EndsWith("/")) baseUrl += "/";
            
            // Remove leading / from endpoint if present to avoid double slashes
            if (endpoint.StartsWith("/")) endpoint = endpoint.Substring(1);

            var url = $"{baseUrl}{endpoint}";

            var request = new HttpRequestMessage(method, url);
            request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

            if (content != null)
            {
                var jsonContent = JsonSerializer.Serialize(content, new JsonSerializerOptions
                {
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                });
                request.Content = new StringContent(jsonContent, Encoding.UTF8, "application/json");
            }

            return request;
        }

        public async Task<List<ProductoStock>> GetAllProductsAsync()
        {
            try
            {
                _logger.LogInformation("🔍 Obteniendo productos desde Stock API...");

                var token = await GetAccessTokenAsync();
                
                var baseUrl = _configuration["ExternalApis:Stock:BaseUrl"];
                if (string.IsNullOrEmpty(baseUrl)) baseUrl = "http://localhost:3000/";
                if (!baseUrl.EndsWith("/")) baseUrl += "/";
                
                // The configured URL is http://gateway:80/stock/productos/
                // So for "GetAll", we just use the base URL.
                var url = baseUrl; 
                
                _logger.LogInformation($"📡 Requesting URL: {url}");

                var request = new HttpRequestMessage(HttpMethod.Get, url);
                request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

                var response = await _httpClient.SendAsync(request);

                if (!response.IsSuccessStatusCode)
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    _logger.LogError($"❌ Error HTTP: {response.StatusCode} - {errorContent}");
                    throw new HttpRequestException($"Error: {response.StatusCode} - {errorContent}");
                }

                var content = await response.Content.ReadAsStringAsync();
                _logger.LogInformation($"📦 Respuesta recibida, longitud: {content.Length} caracteres");

                // La API de Stock devuelve { "data": [ ...productos... ] }
                var responseWrapper = JsonSerializer.Deserialize<StockApiResponse>(content, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });

                if (responseWrapper?.Data != null)
                {
                    _logger.LogInformation($"✅ Obtenidos {responseWrapper.Data.Count} productos REALES de Stock API");
                    return responseWrapper.Data;
                }
                else
                {
                    // Attempt to deserialize as direct list if wrapper fails or data is null
                    try 
                    {
                        var directList = JsonSerializer.Deserialize<List<ProductoStock>>(content, new JsonSerializerOptions
                        {
                            PropertyNameCaseInsensitive = true
                        });
                        if (directList != null) {
                             _logger.LogInformation($"✅ Obtenidos {directList.Count} productos (Lista Directa) de Stock API");
                             return directList;
                        }
                    } catch {}

                    _logger.LogWarning("❌ No se encontraron productos en la respuesta");
                    return new List<ProductoStock>();
                }
            }
            catch (HttpRequestException httpEx)
            {
                _logger.LogError(httpEx, "❌ Error HTTP conectando con Stock API");
                throw;
            }
            catch (JsonException jsonEx)
            {
                _logger.LogError(jsonEx, "❌ Error deserializando JSON de Stock API");
                throw;
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "❌ Error inesperado - Usando datos de prueba");
                return GetProductosDePrueba();
            }
        }

        // También actualiza el método GetProductByIdAsync
        public async Task<ProductoStock> GetProductByIdAsync(int id)
        {
            try
            {
                _logger.LogInformation($"Obteniendo producto {id} desde Stock API...");

                // Reuse CreateAuthenticatedRequest or manual logic?
                // If BaseUrl is http://gateway:80/stock/productos/
                // We want http://gateway:80/stock/productos/{id}
                
                var token = await GetAccessTokenAsync();
                var baseUrl = _configuration["ExternalApis:Stock:BaseUrl"];
                if (!baseUrl.EndsWith("/")) baseUrl += "/";
                
                var url = $"{baseUrl}{id}"; // Assumes BaseUrl ends in /productos/
                
                var request = new HttpRequestMessage(HttpMethod.Get, url);
                request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

                var response = await _httpClient.SendAsync(request);

                if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
                    return null;

                if (!response.IsSuccessStatusCode)
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    _logger.LogError($"Error obteniendo producto {id}. Status: {response.StatusCode}");
                    throw new HttpRequestException($"Error obteniendo producto: {response.StatusCode}");
                }

                var content = await response.Content.ReadAsStringAsync();

                // Para producto individual, probablemente devuelva el objeto directo
                return JsonSerializer.Deserialize<ProductoStock>(content, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });
            }
            catch (HttpRequestException)
            {
                throw;
            }
            catch (JsonException)
            {
                throw;
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, $"Stock API no disponible - Buscando producto {id} en datos de prueba");
                var productos = GetProductosDePrueba();
                return productos.FirstOrDefault(p => p.Id == id);
            }
        }



        // Agrega esta clase para manejar la respuesta de Stock API
        public class StockApiResponse
        {
            [JsonPropertyName("data")]
            public List<ProductoStock> Data { get; set; } = new List<ProductoStock>();
        }

        public Task<ReservaCompleta> ObtenerReservaAsync(int idReserva, int usuarioId)
        {
            throw new NotImplementedException();
        }

        // MÉTODO PARA OBTENER TOKEN DE KEYCLOAK
        private async Task<string> GetAccessTokenAsync()
        {
            // Verificar si el token está en caché y es válido
            if (!string.IsNullOrEmpty(_cachedToken) && DateTime.UtcNow < _tokenExpiry)
            {
                return _cachedToken;
            }

            try
            {
                _logger.LogInformation("Obteniendo token de Keycloak...");

                var tokenEndpoint = _configuration["StockApi:TokenEndpoint"] ?? _configuration["ExternalApis:Logistica:TokenEndpoint"]; // Fallback or use specific key
                // In docker-compose, we only see BaseUrl override.
                // We should probably use a default if not found.
                if (string.IsNullOrEmpty(tokenEndpoint)) 
                    tokenEndpoint = "http://keycloak:8080/realms/ds-2025-realm/protocol/openid-connect/token";

                var clientId = _configuration["StockApi:ClientId"] ?? "grupo-08";
                var clientSecret = _configuration["StockApi:ClientSecret"] ?? "248f42b5-7007-47d1-a94e-e8941f352f6f";

                var tokenRequest = new List<KeyValuePair<string, string>>
                {
                    new("client_id", clientId),
                    new("client_secret", clientSecret),
                    new("grant_type", "client_credentials")
                };

                var content = new FormUrlEncodedContent(tokenRequest);

                // Usar una instancia temporal de HttpClient para evitar conflictos
                using var httpClient = new HttpClient();
                var response = await httpClient.PostAsync(tokenEndpoint, content);

                if (!response.IsSuccessStatusCode)
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    _logger.LogError("Error obteniendo token de Keycloak: {StatusCode} - {Error}",
                        response.StatusCode, errorContent);
                    throw new Exception($"Error obteniendo token: {response.StatusCode}");
                }

                var tokenResponse = await response.Content.ReadFromJsonAsync<KeycloakTokenResponse>();
                _cachedToken = tokenResponse.AccessToken;
                _tokenExpiry = DateTime.UtcNow.AddSeconds(tokenResponse.ExpiresIn - 60); // Restar 60 segundos de margen

                _logger.LogInformation("Token de Keycloak obtenido exitosamente");
                return _cachedToken;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error crítico obteniendo token de Keycloak");
                throw;
            }
        }

        // MÉTODO CON DATOS DE PRUEBA
        private List<ProductoStock> GetProductosDePrueba()
        {
            return new List<ProductoStock>
            {
                new ProductoStock
                {
                    Id = 1,
                    Nombre = "Laptop Gaming",
                    Descripcion = "Laptop para gaming de alta performance",
                    Precio = 1500.00M,
                    StockDisponible = 10,
                    PesoKg = 2.5M,
                    Dimensiones = new Dimensiones { LargoCm = 35.0M, AnchoCm = 25.0M, AltoCm = 2.5M },
                    Ubicacion = new UbicacionAlmacen
                    {
                        Street = "Av. Siempre Viva 123",
                        City = "Resistencia",
                        State = "Chaco",
                        PostalCode = "H3500ABC",
                        Country = "AR"
                    },
                    Categorias = new List<Categoria>
                    {
                        new Categoria { Id = 1, Nombre = "Electrónica", Descripcion = "Productos electrónicos" }
                    }
                },
                new ProductoStock
                {
                    Id = 2,
                    Nombre = "Mouse Inalámbrico",
                    Descripcion = "Mouse ergonómico inalámbrico",
                    Precio = 45.50M,
                    StockDisponible = 25,
                    PesoKg = 0.2M,
                    Dimensiones = new Dimensiones { LargoCm = 12.0M, AnchoCm = 6.0M, AltoCm = 3.0M },
                    Ubicacion = new UbicacionAlmacen
                    {
                        Street = "Av. Vélez Sársfield 456",
                        City = "Resistencia",
                        State = "Chaco",
                        PostalCode = "H3500XYZ",
                        Country = "AR"
                    },
                    Categorias = new List<Categoria>
                    {
                        new Categoria { Id = 1, Nombre = "Electrónica", Descripcion = "Productos electrónicos" },
                        new Categoria { Id = 2, Nombre = "Accesorios", Descripcion = "Accesorios para computadora" }
                    }
                }
            };
        }
    }

    // Model para la respuesta del token
    public class KeycloakTokenResponse
    {
        [JsonPropertyName("access_token")]
        public string AccessToken { get; set; }

        [JsonPropertyName("expires_in")]
        public int ExpiresIn { get; set; }

        [JsonPropertyName("token_type")]
        public string TokenType { get; set; }

        [JsonPropertyName("scope")]
        public string Scope { get; set; }
    }
}
