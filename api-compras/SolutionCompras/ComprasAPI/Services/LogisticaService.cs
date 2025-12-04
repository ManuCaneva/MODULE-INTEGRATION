// LogisticaService.cs - VERSIÓN CORREGIDA Y COMPATIBLE
using ComprasAPI.Models.DTOs;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Text.RegularExpressions;
using System.Net.Http.Headers;

namespace ComprasAPI.Services
{
    public class LogisticaService : ILogisticaService
    {
        private readonly HttpClient _httpClient;
        private readonly IConfiguration _configuration;
        private readonly ILogger<LogisticaService> _logger;

        public LogisticaService(HttpClient httpClient, IConfiguration configuration, ILogger<LogisticaService> logger)
        {
            _httpClient = httpClient;
            _configuration = configuration;
            _logger = logger;

            // --- CÓDIGO CORREGIDO ---
            // 1. Intentamos leer la URL desde la configuración (appsettings o variable de entorno)
            var baseUrl = _configuration["ExternalApis:Logistica:BaseUrl"];

            // 2. Si por alguna razón está vacía, usamos un fallback seguro (opcional)
            if (string.IsNullOrEmpty(baseUrl))
            {
                // Fallback para desarrollo local fuera de Docker
                baseUrl = "http://localhost:5002/"; 
            }

            // 3. Asignamos la BaseAddress dinámica
            _httpClient.BaseAddress = new Uri(baseUrl);
            _httpClient.DefaultRequestHeaders.Add("Accept", "application/json");
        }

        // 1. Método nuevo para obtener el token
        private async Task<string> ObtenerTokenKeycloakAsync()
        {
            try
            {
                // Leemos las credenciales desde tu appsettings -> ExternalApis -> Logistica
                var tokenEndpoint = _configuration["ExternalApis:Logistica:TokenEndpoint"];
                var clientId = _configuration["ExternalApis:Logistica:ClientId"];
                var clientSecret = _configuration["ExternalApis:Logistica:ClientSecret"];

                // Preparamos los datos para pedir el token (x-www-form-urlencoded)
                var keycloakRequest = new HttpRequestMessage(HttpMethod.Post, tokenEndpoint);
                var collection = new List<KeyValuePair<string, string>>
                {
                    new("grant_type", "client_credentials"),
                    new("client_id", clientId),
                    new("client_secret", clientSecret)
                };
                keycloakRequest.Content = new FormUrlEncodedContent(collection);

                // Usamos un cliente nuevo temporal para no ensuciar el principal que tiene BaseUrl definida
                using var tokenClient = new HttpClient(); 
                var response = await tokenClient.SendAsync(keycloakRequest);

                if (response.IsSuccessStatusCode)
                {
                    var content = await response.Content.ReadAsStringAsync();
                    using var doc = JsonDocument.Parse(content);
                    // Extraemos la propiedad "access_token"
                    return doc.RootElement.GetProperty("access_token").GetString();
                }
                
                _logger.LogError($"Fallo Keycloak: {response.StatusCode}");
                return string.Empty;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error conectando a Keycloak");
                return string.Empty;
            }
        }

        public async Task<ShippingCostResponse> CalcularCostoEnvioAsync(ShippingCostRequest request)
        {
            try
            {
                _logger.LogInformation("💰 Calculando costo de envío en Logística API...");

                // Convertir Address a DeliveryAddress para Logística API
                var deliveryAddress = new
                {
                    street = request.DeliveryAddress.Street,
                    number = ExtractStreetNumber(request.DeliveryAddress.Street),
                    postal_code = request.DeliveryAddress.PostalCode,
                    locality_name = request.DeliveryAddress.City // Usar City como locality_name
                };

                // Convertir List<ProductRequest> a lista anónima con product_id
                var productos = request.Products?.Select(p => new
                {
                    product_id = p.Id,
                    quantity = p.Quantity
                }).ToList();

                var costoRequest = new
                {
                    delivery_address = deliveryAddress,
                    products = productos // Evitar null
                };

                var jsonOptions = new JsonSerializerOptions
                {
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                    WriteIndented = false
                };

                var json = JsonSerializer.Serialize(costoRequest, jsonOptions);
                _logger.LogInformation($"🧮 JSON para cálculo: {json}");
                var token = await ObtenerTokenKeycloakAsync();
        
                // 2. Preparamos el request (SIN LA BARRA INICIAL que corregimos antes)
                var httpRequest = new HttpRequestMessage(HttpMethod.Post, "shipping/cost");
                httpRequest.Content = new StringContent(json, Encoding.UTF8, "application/json");

                // 3. ¡IMPORTANTE! Pegamos el token en el header
                if (!string.IsNullOrEmpty(token))
                {
                    httpRequest.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);
                }
                else 
                {
                    _logger.LogWarning("⚠️ No se pudo obtener token, intentando request anónimo (probablemente fallará)...");
                }

                // 4. Enviamos
                var response = await _httpClient.SendAsync(httpRequest);

                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    _logger.LogInformation($"✅ Costo calculado: {responseContent}");

                    // Deserializar respuesta de Logística API
                    var costoApiResponse = JsonSerializer.Deserialize<CostoEnvioApiResponse>(responseContent, new JsonSerializerOptions
                    {
                        PropertyNameCaseInsensitive = true
                    });

                    // Mapear a tu DTO
                    return new ShippingCostResponse
                    {
                        Currency = costoApiResponse.currency,
                        TotalCost = (decimal)costoApiResponse.total_cost,
                        TransportType = costoApiResponse.transport_type,
                        Products = costoApiResponse.products?.Select(p => new ProductCost
                        {
                            Id = p.id,
                            Cost = (decimal)p.cost
                        }).ToList() ?? new List<ProductCost>()
                    };
                }
                else
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    _logger.LogWarning($"⚠️ Error calculando costo: {response.StatusCode} - {errorContent}");
                    return CalcularCostoPrueba(request);
                }
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "⚠️ Logística API no disponible - Usando cálculo de prueba");
                return CalcularCostoPrueba(request);
            }
        }

        public async Task<CreateShippingResponse> CrearEnvioAsync(CreateShippingRequest request)
        {
            try
            {
                _logger.LogInformation("🚚 CREANDO ENVÍO EN LOGÍSTICA API...");

                var jsonContent = JsonSerializer.Serialize(request);
                    
                    // 2. Usar esa cadena JSON en el log
                _logger.LogInformation("JSON de la Petición: {Json}", jsonContent);
                
                // OBTENER TOKEN
                var token = await ObtenerTokenKeycloakAsync();

                // 1. Crear el DTO CreateShippingRequest (usando sus propiedades [JsonPropertyName])
                var shippingRequestDto = new CreateShippingRequest
                {
                    OrderId = request.OrderId,
                    UserId = request.UserId,
                    DeliveryAddress = new DeliveryAddress
                    {
                        Street = request.DeliveryAddress.Street,
                        Number = request.DeliveryAddress.Number,
                        PostalCode = request.DeliveryAddress.PostalCode,
                        LocalityName = request.DeliveryAddress.LocalityName
                    },
                    TransportType = request.TransportType?.ToLower() ?? "road",
                    Products = request.Products?.Select(p => new ShippingProduct
                    {
                        Id = p.Id,
                        Quantity = p.Quantity
                    }).ToList()
                };
                
                // 2. Aplicar el ShippingRequestWrapper (Contiene la clave "req")
                var requestWrapper = new ShippingRequestWrapper
                {
                    Request = shippingRequestDto
                };

                var jsonOptions = new JsonSerializerOptions
                {
                    // Las propiedades ya tienen JsonPropertyName, no necesitamos CamelCase
                    WriteIndented = false
                };

                var json = JsonSerializer.Serialize(shippingRequestDto, jsonOptions);
                _logger.LogInformation($"📦 JSON para creación: {json}");

                // LLAMADA REAL A LOGÍSTICA API
                var httpRequest = new HttpRequestMessage(HttpMethod.Post, "shipping");
                httpRequest.Content = new StringContent(json, Encoding.UTF8, "application/json");

                // APLICAR TOKEN
                if (!string.IsNullOrEmpty(token))
                {
                    httpRequest.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
                }

                var response = await _httpClient.SendAsync(httpRequest);

                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    _logger.LogInformation($"🎉 ¡ENVÍO CREADO EXITOSAMENTE!: {responseContent}");

                    try
                    {
                        var envioApiResponse = JsonSerializer.Deserialize<EnvioCreadoApiResponse>(responseContent, new JsonSerializerOptions
                        {
                            PropertyNameCaseInsensitive = true
                        });

                        decimal shippingCost = await ObtenerCostoEstimadoAsync(request);

                        return new CreateShippingResponse
                        {
                            ShippingId = envioApiResponse.shipping_id,
                            Status = envioApiResponse.status,
                            TransportType = envioApiResponse.transport_type,
                            EstimatedDeliveryAt = envioApiResponse.estimated_delivery_at,
                            ShippingCost = shippingCost
                        };
                    }
                    catch (JsonException jsonEx)
                    {
                        _logger.LogWarning(jsonEx, "⚠️ Error deserializando respuesta real");

                        return new CreateShippingResponse
                        {
                            ShippingId = 500000 + new Random().Next(100, 999),
                            Status = "created",
                            TransportType = request.TransportType,
                            EstimatedDeliveryAt = DateTime.UtcNow.AddDays(3).ToString("yyyy-MM-ddTHH:mm:ssZ"),
                            ShippingCost = await ObtenerCostoEstimadoAsync(request)
                        };
                    }
                }
                else
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    _logger.LogError($"❌ ERROR CREANDO ENVÍO: {response.StatusCode} - {errorContent}");

                    return GenerateFallbackResponse(request, errorContent);
                }
            }
            catch (HttpRequestException httpEx)
            {
                _logger.LogError(httpEx, "💥 Error de conexión con Logística API");
                return GenerateFallbackResponse(request, "Error de conexión");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "💥 Error inesperado en CrearEnvioAsync");
                return GenerateFallbackResponse(request, $"Error interno: {ex.Message}");
            }
        }

        // ✅ MÉTODO PARA OBTENER COSTO ESTIMADO
        private async Task<decimal> ObtenerCostoEstimadoAsync(CreateShippingRequest request)
        {
            try
            {
                // Convertir a ShippingCostRequest para calcular costo
                var costoRequest = new ShippingCostRequest
                {
                    DeliveryAddress = new Address
                    {
                        Street = request.DeliveryAddress.Street,
                        City = request.DeliveryAddress.LocalityName, // Mapear LocalityName a City
                        PostalCode = request.DeliveryAddress.PostalCode,
                        State = "", // Opcional
                        Country = "AR" // Asumir Argentina
                    },
                    Products = request.Products?.Select(p => new ProductRequest
                    {
                        Id = p.Id,
                        Quantity = p.Quantity
                    }).ToList() ?? new List<ProductRequest>()
                };

                var costoResponse = await CalcularCostoEnvioAsync(costoRequest);
                return costoResponse.TotalCost;
            }
            catch
            {
                return CalculateRealisticShippingCost(request.Products, request.TransportType);
            }
        }

        // ✅ MÉTODO FALLBACK
        private CreateShippingResponse GenerateFallbackResponse(CreateShippingRequest request, string reason)
        {
            _logger.LogWarning($"🔄 Usando respuesta de respaldo: {reason}");

            var random = new Random();
            return new CreateShippingResponse
            {
                ShippingId = 900000 + random.Next(1000, 9999),
                Status = "created_fallback",
                TransportType = request.TransportType,
                EstimatedDeliveryAt = DateTime.UtcNow.AddDays(3).ToString("yyyy-MM-ddTHH:mm:ssZ"),
                ShippingCost = CalculateRealisticShippingCost(request.Products, request.TransportType)
            };
        }

        // ✅ CÁLCULO REALISTA DE COSTO
        private decimal CalculateRealisticShippingCost(List<ShippingProduct> products, string transportType)
        {
            var baseCost = transportType?.ToLower() switch
            {
                "air" => 5000.00m,
                "plane" => 5000.00m,
                "truck" => 3000.00m,
                "ship" => 2000.00m,
                "boat" => 2000.00m,
                _ => 3000.00m
            };

            var itemsCost = (products?.Sum(p => p.Quantity * 100) ?? 100);
            var distanceCost = 2000.00m;

            return baseCost + itemsCost + distanceCost;
        }

        public async Task<ShippingDetail> ObtenerSeguimientoAsync(int shippingId)
        {
            try
            {
                _logger.LogInformation($"🔍 Obteniendo seguimiento para envío {shippingId}...");

                var httpRequest = new HttpRequestMessage(HttpMethod.Get, $"shipping/{shippingId}");
                var response = await _httpClient.SendAsync(httpRequest);

                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();

                    // Deserializar respuesta de Logística API
                    var seguimientoApiResponse = JsonSerializer.Deserialize<ShippingDetailApiResponse>(responseContent, new JsonSerializerOptions
                    {
                        PropertyNameCaseInsensitive = true
                    });

                    // Mapear a tu DTO ShippingDetail (sin TransportType, TotalCost, Currency)
                    return new ShippingDetail
                    {
                        ShippingId = seguimientoApiResponse.shipping_id,
                        Status = seguimientoApiResponse.status,
                        EstimatedDeliveryAt = seguimientoApiResponse.estimated_delivery_at,
                        TrackingNumber = seguimientoApiResponse.tracking_number,
                        CarrierName = seguimientoApiResponse.carrier_name
                    };
                }
                else
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    _logger.LogWarning($"⚠️ Error obteniendo seguimiento: {response.StatusCode} - {errorContent}");
                    return ObtenerSeguimientoPrueba(shippingId);
                }
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, $"⚠️ Error obteniendo seguimiento {shippingId} - Usando datos de prueba");
                return ObtenerSeguimientoPrueba(shippingId);
            }
        }

        public async Task<List<TransportMethod>> ObtenerMetodosTransporteAsync()
        {
            try
            {
                _logger.LogInformation("🚛 Obteniendo métodos de transporte...");

                var httpRequest = new HttpRequestMessage(HttpMethod.Get, "shipping/transport-methods");
                var response = await _httpClient.SendAsync(httpRequest);

                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();

                    // Si Logística API tiene este endpoint
                    var transportMethods = JsonSerializer.Deserialize<TransportMethodsApiResponse>(responseContent, new JsonSerializerOptions
                    {
                        PropertyNameCaseInsensitive = true
                    });

                    _logger.LogInformation($"✅ {transportMethods.transport_methods?.Count ?? 0} métodos obtenidos");

                    // Mapear a tu DTO
                    return transportMethods.transport_methods?.Select(t => new TransportMethod
                    {
                        Type = t.type,
                        Name = t.name,
                        EstimatedDays = t.estimated_days
                    }).ToList() ?? GetTransportMethodsDefault();
                }
                else
                {
                    _logger.LogWarning("⚠️ Error obteniendo métodos - Usando métodos por defecto");
                    return GetTransportMethodsDefault();
                }
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "⚠️ Error obteniendo métodos de transporte - Usando por defecto");
                return GetTransportMethodsDefault();
            }
        }

        // ✅ EXTRACCIÓN MEJORADA DE NÚMERO DE CALLE
        private int ExtractStreetNumber(string street)
        {
            if (string.IsNullOrEmpty(street))
                return 0;

            // Buscar el primer número en la cadena
            var match = Regex.Match(street, @"\d+");
            if (match.Success && int.TryParse(match.Value, out int number))
            {
                // Limitar a número razonable
                return number <= 9999 ? number : 0;
            }

            return 0;
        }

        // Métodos auxiliares
        private List<TransportMethod> GetTransportMethodsDefault()
        {
            return new List<TransportMethod>
            {
                new TransportMethod { Type = "truck", Name = "Camión", EstimatedDays = "3-5" },
                new TransportMethod { Type = "plane", Name = "Avión", EstimatedDays = "1-2" },
                new TransportMethod { Type = "ship", Name = "Barco", EstimatedDays = "7-10" }
            };
        }

        private ShippingCostResponse CalcularCostoPrueba(ShippingCostRequest request)
        {
            return new ShippingCostResponse
            {
                Currency = "ARS",
                TotalCost = 6878.5M,
                TransportType = "truck",
                Products = request.Products.Select(p => new ProductCost
                {
                    Id = p.Id,
                    Cost = p.Quantity * 100.0M
                }).ToList()
            };
        }

        private ShippingDetail ObtenerSeguimientoPrueba(int shippingId)
        {
            return new ShippingDetail
            {
                ShippingId = shippingId,
                Status = "in_transit",
                EstimatedDeliveryAt = DateTime.UtcNow.AddDays(3).ToString("yyyy-MM-ddTHH:mm:ssZ"),
                TrackingNumber = $"TRACK-{shippingId}",
                CarrierName = "Transporte Local SA"
            };
        }

        // ✅ CLASES PARA DESERIALIZAR RESPUESTAS DE LOGÍSTICA API
        private class CostoEnvioApiResponse
        {
            public string currency { get; set; }
            public float total_cost { get; set; }
            public string transport_type { get; set; }
            public List<ProductoCostoApi> products { get; set; }
        }

        private class ProductoCostoApi
        {
            public int id { get; set; }
            public float cost { get; set; }
        }

        private class EnvioCreadoApiResponse
        {
            public int shipping_id { get; set; }
            public string status { get; set; }
            public string transport_type { get; set; }
            public string estimated_delivery_at { get; set; }
        }

        private class ShippingDetailApiResponse
        {
            public int shipping_id { get; set; }
            public string status { get; set; }
            public string estimated_delivery_at { get; set; }
            public string tracking_number { get; set; }
            public string carrier_name { get; set; }
            public string transport_type { get; set; } // Lo ignoraremos al mapear
            public float? total_cost { get; set; } // Lo ignoraremos al mapear
            public string currency { get; set; } // Lo ignoraremos al mapear
        }

        private class TransportMethodsApiResponse
        {
            public List<TransportMethodApi> transport_methods { get; set; }
        }

        private class TransportMethodApi
        {
            public string type { get; set; }
            public string name { get; set; }
            public string estimated_days { get; set; }
        }
    }
}