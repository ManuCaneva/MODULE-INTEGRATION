// Services/LogisticaService.cs
using ComprasAPI.Models.DTOs;
using System.Text;
using System.Text.Json;

namespace ComprasAPI.Services
{
    public class LogisticaService : ILogisticaService
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<LogisticaService> _logger;

        public LogisticaService(HttpClient httpClient, ILogger<LogisticaService> logger)
        {
            _httpClient = httpClient;
            _logger = logger;
        }

        public async Task<ShippingCostResponse> CalcularCostoEnvioAsync(ShippingCostRequest request)
        {
            try
            {
                _logger.LogInformation(" Calculando costo de envío...");

                var json = JsonSerializer.Serialize(request);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync("shipping/cost", content);
                response.EnsureSuccessStatusCode();

                var responseContent = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<ShippingCostResponse>(responseContent, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, " Logística API no disponible - Usando cálculo de prueba");
                return CalcularCostoPrueba(request);
            }
        }

        public async Task<CreateShippingResponse> CrearEnvioAsync(CreateShippingRequest request)
        {
            try
            {
                _logger.LogInformation(" Creando envío en Logística API...");

                var json = JsonSerializer.Serialize(request);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync("/shipping", content);
                response.EnsureSuccessStatusCode();

                var responseContent = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<CreateShippingResponse>(responseContent, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, " Logística API no disponible - Creando envío de prueba");
                return CrearEnvioPrueba(request);
            }
        }

        public async Task<ShippingDetail> ObtenerSeguimientoAsync(int shippingId)
        {
            try
            {
                _logger.LogInformation($" Obteniendo seguimiento para envío {shippingId}...");

                var response = await _httpClient.GetAsync($"/shipping/{shippingId}");
                response.EnsureSuccessStatusCode();

                var responseContent = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<ShippingDetail>(responseContent, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, $" Error obteniendo seguimiento {shippingId}");
                return ObtenerSeguimientoPrueba(shippingId);
            }
        }

        public async Task<List<TransportMethod>> ObtenerMetodosTransporteAsync()
        {
            try
            {
                _logger.LogInformation(" Obteniendo métodos de transporte...");

                var response = await _httpClient.GetAsync("/shipping/transport-methods");
                response.EnsureSuccessStatusCode();

                var responseContent = await response.Content.ReadAsStringAsync();
                var result = JsonSerializer.Deserialize<TransportMethodsResponse>(responseContent, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });

                return result?.TransportMethods ?? new List<TransportMethod>();
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, " Error obteniendo métodos de transporte - Usando datos de prueba");
                return ObtenerMetodosTransportePrueba();
            }
        }

        // Métodos de prueba para cuando la API no está disponible
        private ShippingCostResponse CalcularCostoPrueba(ShippingCostRequest request)
        {
            return new ShippingCostResponse
            {
                Currency = "ARS",
                TotalCost = 45.50M,
                TransportType = "road",
                Products = request.Products.Select(p => new ProductCost
                {
                    Id = p.Id,
                    Cost = p.Quantity * 10.0M
                }).ToList()
            };
        }

        private CreateShippingResponse CrearEnvioPrueba(CreateShippingRequest request)
        {
            return new CreateShippingResponse
            {
                ShippingId = new Random().Next(1000, 9999),
                Status = "created",
                TransportType = request.TransportType,
                EstimatedDeliveryAt = DateTime.UtcNow.AddDays(5).ToString("yyyy-MM-ddTHH:mm:ssZ")
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
                CarrierName = "Transporte de Prueba SA"
            };
        }

        private List<TransportMethod> ObtenerMetodosTransportePrueba()
        {
            return new List<TransportMethod>
            {
                new TransportMethod { Type = "road", Name = "Transporte Terrestre", EstimatedDays = "3-5" },
                new TransportMethod { Type = "air", Name = "Transporte Aéreo", EstimatedDays = "1-2" },
                new TransportMethod { Type = "rail", Name = "Transporte Ferroviario", EstimatedDays = "5-7" }
            };
        }
    }
}
