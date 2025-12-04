// Controllers/TestIntegrationController.cs (corregido)
using ComprasAPI.Models.DTOs;
using ComprasAPI.Services;
using Microsoft.AspNetCore.Mvc;

namespace ComprasAPI.Controllers
{
    [ApiController]
    [Route("api/test")]
    public class TestIntegrationController : ControllerBase
    {
        private readonly IStockService _stockService;
        private readonly ILogisticaService _logisticaService;
        private readonly ILogger<TestIntegrationController> _logger;

        public TestIntegrationController(
            IStockService stockService,
            ILogisticaService logisticaService,
            ILogger<TestIntegrationController> logger)
        {
            _stockService = stockService;
            _logisticaService = logisticaService;
            _logger = logger;
        }

        [HttpGet("stock")]
        public async Task<IActionResult> TestStock()
        {
            try
            {
                _logger.LogInformation(" Probando conexión con Stock...");

                var productos = await _stockService.GetAllProductsAsync();

                return Ok(new
                {
                    message = " Stock Service funcionando",
                    productosCount = productos.Count,
                    productos = productos.Take(3),
                    source = productos.Any() ? "Stock API" : "Datos de prueba"
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new
                {
                    error = " Error con Stock Service",
                    details = ex.Message,
                    source = "Fallback a datos de prueba"
                });
            }
        }

        [HttpPost("stock/create-reservation")]
        public async Task<IActionResult> TestCreateReservation()
        {
            try
            {
                _logger.LogInformation(" Probando creación de reserva...");

                var reservaInput = new ReservaInput
                {
                    IdCompra = "TEST-" + Guid.NewGuid().ToString(),
                    UsuarioId = 1,
                    Productos = new List<ProductoReserva>
                    {
                        new ProductoReserva { IdProducto = 1, Cantidad = 2 },
                        new ProductoReserva { IdProducto = 2, Cantidad = 1 }
                    }
                };

                var resultado = await _stockService.CrearReservaAsync(reservaInput);

                return Ok(new
                {
                    message = " Creación de reserva funcionando",
                    reservaInput = reservaInput,
                    resultado = resultado,
                    source = resultado.IdReserva > 0 ? "Stock API" : "Datos de prueba"
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new
                {
                    error = " Error creando reserva",
                    details = ex.Message,
                    source = "Fallback a datos de prueba"
                });
            }
        }

        [HttpGet("logistica/transport-methods")]
        public async Task<IActionResult> TestLogisticaTransport()
        {
            try
            {
                _logger.LogInformation(" Probando métodos de transporte...");

                var metodos = await _logisticaService.ObtenerMetodosTransporteAsync();

                return Ok(new
                {
                    message = " Logística Service funcionando",
                    metodosCount = metodos.Count,
                    metodos = metodos,
                    source = metodos.Any() ? "Logística API" : "Datos de prueba"
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new
                {
                    error = " Error con Logística Service",
                    details = ex.Message,
                    source = "Fallback a datos de prueba"
                });
            }
        }
        [HttpPost("logistica/calculate-shipping-dynamic")]
        public async Task<IActionResult> CalculateShippingDynamic([FromBody] ShippingCostRequest request)
        {
            try
            {
                _logger.LogInformation("🧮 Calculando envío con datos personalizados...");

                // Validamos que el body no sea nulo
                if (request == null || request.DeliveryAddress == null)
                {
                    return BadRequest("El cuerpo de la solicitud no es válido.");
                }

                var resultado = await _logisticaService.CalcularCostoEnvioAsync(request);

                return Ok(new
                {
                    message = "Cálculo exitoso",
                    input_recibido = request,
                    resultado_logistica = resultado
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error en endpoint dinámico de logística");
                return StatusCode(500, new { error = ex.Message });
            }
        }

        // 2. Endpoint para probar la conexión con Stock API (Obtener Productos)
        [HttpGet("stock/products")]
        public async Task<IActionResult> GetStockProducts()
        {
            try
            {
                _logger.LogInformation("📦 Solicitando lista de productos a Stock API...");

                var productos = await _stockService.GetAllProductsAsync();

                return Ok(new
                {
                    message = $"Se obtuvieron {productos.Count} productos desde Stock API",
                    productos = productos
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error conectando con Stock API");
                return StatusCode(500, new { error = ex.Message });
            }
        }
        [HttpGet("logistica/shipments/{id}")]
        public async Task<IActionResult> GetShipmentById(int id)
        {
            try
            {
                _logger.LogInformation($"🔎 Buscando envío {id}...");
                var result = await _logisticaService.ObtenerSeguimientoAsync(id);
                
                // Si devuelve el ID, asumimos éxito (ajusta según tu lógica de retorno de error)
                if (result != null && result.ShippingId > 0)
                    return Ok(new { message = "Encontrado", data = result });
                else
                    return NotFound(new { message = "No se encontró el envío o hubo error" });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }
        /*
        // 4. Prueba Búsqueda con Filtros (GET shipping?...)
        [HttpGet("logistica/shipments")]
        public async Task<IActionResult> GetShipmentsFiltered(
            [FromQuery] int? userId,
            [FromQuery] string? status,
            [FromQuery] DateTime? fromDate,
            [FromQuery] DateTime? toDate,
            [FromQuery] int page = 1,
            [FromQuery] int limit = 10)
        {
            try
            {
                _logger.LogInformation("🔎 Probando filtros de envíos...");
                var result = await _logisticaService.ObtenerEnviosFiltradosAsync(userId, status, fromDate, toDate, page, limit);
                return Ok(new { message = "Respuesta de Logística", data = result });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }
        */
      // 5. Prueba Cancelar Envío (POST logistica/shipments/{id}/cancel)
        [HttpPost("logistica/shipments/{id}/cancel")]
        public async Task<IActionResult> CancelShipment(int id)
        {
            try
            {
                _logger.LogInformation($"🛑 Solicitando cancelación para envío {id}...");
                
                var exito = await _logisticaService.CancelarEnvioAsync(id);

                if (exito)
                {
                    return Ok(new { message = $"Envío {id} cancelado exitosamente." });
                }
                else
                {
                    return BadRequest(new { message = $"No se pudo cancelar el envío {id}. Verifique si existe o si ya fue entregado." });
                }
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }
        [HttpPost("logistica/calculate-shipping")]
        public async Task<IActionResult> TestCalculateShipping()
        {
            try
            {
                _logger.LogInformation(" Probando cálculo de envío...");

                var request = new ShippingCostRequest
                {
                    DeliveryAddress = new Address
                    {
                        Street = "Av. Siempre Viva 123",
                        City = "Resistencia",
                        State = "Chaco",
                        PostalCode = "H3500ABC",
                        Country = "AR"
                    },
                    Products = new List<ProductRequest>
                    {
                        new ProductRequest { Id = 1, Quantity = 2 },
                        new ProductRequest { Id = 2, Quantity = 1 }
                    }
                };

                var resultado = await _logisticaService.CalcularCostoEnvioAsync(request);

                return Ok(new
                {
                    message = " Cálculo de envío funcionando",
                    request = request,
                    resultado = resultado,
                    source = resultado.TotalCost > 0 ? "Logística API" : "Datos de prueba"
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new
                {
                    error = " Error calculando envío",
                    details = ex.Message,
                    source = "Fallback a datos de prueba"
                });
            }
        }

        [HttpGet("integration-status")]
        public async Task<IActionResult> GetIntegrationStatus()
        {
            var status = new
            {
                Timestamp = DateTime.UtcNow,
                ComprasAPI = " Running",
                StockService = await TestStockInternal(),
                LogisticaService = await TestLogisticaInternal(),
                NextSteps = new[]
                {
                    "1. Verificar que los servicios responden",
                    "2. Probar endpoints individuales",
                    "3. Probar flujo completo de checkout",
                    "4. Configurar APIs externas cuando estén listas"
                }
            };

            return Ok(status);
        }

        private async Task<string> TestStockInternal()
        {
            try
            {
                var productos = await _stockService.GetAllProductsAsync();
                return productos.Any() ? " Con datos" : " Sin datos (usando fallback)";
            }
            catch
            {
                return " Error (usando fallback)";
            }
        }

        private async Task<string> TestLogisticaInternal()
        {
            try
            {
                var metodos = await _logisticaService.ObtenerMetodosTransporteAsync();
                return metodos.Any() ? " Con datos" : " Sin datos (usando fallback)";
            }
            catch
            {
                return " Error (usando fallback)";
            }
        }
    }
}