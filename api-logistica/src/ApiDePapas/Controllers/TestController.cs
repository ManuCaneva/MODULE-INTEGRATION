using ApiDePapas.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;
using ApiDePapas.Domain.Entities; // ¡Para que entienda ProductQty!

namespace ApiDePapas.Controllers
{
    [ApiController]
    [Route("api/test")]
    public class TestController : ControllerBase
    {
        private readonly IStockService _stockService;

        // Inyectamos el servicio de Stock (que ahora es el StockApiClient real)
        public TestController(IStockService stockService)
        {
            _stockService = stockService;
        }

        // Creamos un endpoint nuevo para esta prueba
        [HttpGet("test-stock")]
        public async Task<IActionResult> TestStockCall()
        {
            try
            {
                // ¡Asegurate de que el '123' sea un ID de producto que EXISTA
                // en la base de datos de prueba de STOCK!
                
                // --- ¡ESTA ES LA LÍNEA CORREGIDA! ---
                // Usamos el constructor (int, int) como pide el error CS7036
                var productQty = new ProductQty(id: 1, quantity: 1);
                
                // 1. Intentamos usar el StockApiClient
                var productDetail = await _stockService.GetProductDetailAsync(productQty);

                // 2. Si lo logra, nos devuelve los datos del producto
                return Ok(productDetail);
            }
            catch (System.Exception ex)
            {
                // Si falla (Keycloak, DNS, o la API de Stock), nos da el error
                return StatusCode(500, new { error = "No se pudo llamar a Stock.", message = ex.Message, inner = ex.InnerException?.Message });
            }
        }
    }
}