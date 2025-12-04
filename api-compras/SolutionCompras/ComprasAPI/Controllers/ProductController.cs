using Microsoft.AspNetCore.Mvc;
using ComprasAPI.Services;

namespace ComprasAPI.Controllers
{
    [ApiController]
    [Route("api/product")]
    public class ProductController : ControllerBase
    {
        private readonly IStockService _stockService;
        private readonly ILogger<ProductController> _logger;

        public ProductController(IStockService stockService, ILogger<ProductController> logger)
        {
            _stockService = stockService;
            _logger = logger;
        }

        // GET: api/product
        [HttpGet]
        public async Task<IActionResult> GetAllProducts()
        {
            try
            {
                _logger.LogInformation(" Solicitando todos los productos desde Stock API...");

                var productos = await _stockService.GetAllProductsAsync();

                _logger.LogInformation($" Devueltos {productos.Count} productos");
                return Ok(productos);
            }
            catch (System.Net.Http.HttpRequestException ex)
            {
                _logger.LogError(ex, $" No se pudo conectar con Stock API: {ex.Message}");
                
                if (ex.Message.Contains("401") || ex.Message.Contains("403"))
                {
                     return StatusCode(401, new { error = "No autorizado en Stock API", code = "STOCK_AUTH_ERROR" });
                }
                
                return StatusCode(502, new
                {
                    error = $"Servicio Stock no disponible: {ex.Message}",
                    code = "STOCK_SERVICE_UNAVAILABLE"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, " Error interno al obtener productos");
                return StatusCode(500, new
                {
                    error = "Error interno del servidor",
                    code = "INTERNAL_ERROR"
                });
            }
        }

        // GET: api/product/{id}
        [HttpGet("{id}")]
        public async Task<IActionResult> GetProduct(int id)
        {
            try
            {
                _logger.LogInformation($" Solicitando producto ID: {id} desde Stock API");

                var producto = await _stockService.GetProductByIdAsync(id);

                if (producto == null)
                {
                    _logger.LogWarning($" Producto {id} no encontrado");
                    return NotFound(new
                    {
                        error = "Producto no encontrado",
                        code = "PRODUCT_NOT_FOUND"
                    });
                }

                _logger.LogInformation($" Producto {id} encontrado: {producto.Nombre}");
                return Ok(producto);
            }
            catch (System.Net.Http.HttpRequestException ex) when (ex.Message.Contains("404"))
            {
                return NotFound(new
                {
                    error = "Producto no encontrado",
                    code = "PRODUCT_NOT_FOUND"
                });
            }
            catch (System.Net.Http.HttpRequestException ex)
            {
                _logger.LogError(ex, " No se pudo conectar con Stock API");
                return StatusCode(502, new
                {
                    error = "Servicio Stock no disponible",
                    code = "STOCK_SERVICE_UNAVAILABLE"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $" Error al obtener producto {id}");
                return StatusCode(500, new
                {
                    error = "Error interno del servidor",
                    code = "INTERNAL_ERROR"
                });
            }
        }
    }
}