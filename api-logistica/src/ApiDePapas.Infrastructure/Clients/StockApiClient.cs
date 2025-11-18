using ApiDePapas.Application.Interfaces;
using ApiDePapas.Domain.Entities;  // Para ProductDetail y ProductQty
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using System.Text.Json;
using Microsoft.Extensions.Configuration; // Para leer appsettings.json
using System;
using Microsoft.Extensions.Logging; // Para logging

namespace ApiDePapas.Infrastructure.Clients
{
    /**
     * Cliente HTTP (Implementación) para comunicarse con la API de Stock.
     * Implementa el contrato 'IStockService' de la capa de Aplicación.
     */
    public class StockApiClient : IStockService
    {
        private readonly HttpClient _httpClient;
        private readonly ITokenService _tokenService;
        private readonly ILogger<StockApiClient> _logger;

        public StockApiClient(
            HttpClient httpClient, 
            ITokenService tokenService, 
            IConfiguration configuration,
            ILogger<StockApiClient> logger)
        {
            _httpClient = httpClient;
            _tokenService = tokenService;
            _logger = logger;
            
            // Lee la URL base ("http://host.docker.internal:3001/productos/") 
            // desde tu appsettings.json (Con URL de Stock)
            var baseUrl = configuration["StockApi:BaseUrl"];
            if (string.IsNullOrEmpty(baseUrl))
            {
                throw new ArgumentNullException(nameof(baseUrl), "No se encontró 'StockApi:BaseUrl' en la configuración.");
            }
            _httpClient.BaseAddress = new Uri(baseUrl); 
        }

        // Esta es la implementación del método de tu interfaz
        public async Task<ProductDetail> GetProductDetailAsync(ProductQty product)
        {
            if (product == null)
                throw new ArgumentNullException(nameof(product));

            _logger.LogInformation("Llamando a Stock API para ProductId: {ProductId}", product.id);

            // 1. Obtener el token (de caché o nuevo)
            //    Acá es donde llama a tu KeycloakTokenService (que ya corregiste para el Scope)
            var token = await _tokenService.GetAccessTokenAsync();
            
            // DIAGNÓSTICO AÑADIDO: Registrar el token y decodificar el payload para ver los scopes y el issuer.
            if (!string.IsNullOrEmpty(token))
            {
                var parts = token.Split('.');
                if (parts.Length == 3)
                {
                    var payloadBase64 = parts[1];
                    // Aseguramos que la longitud sea múltiplo de 4 para decodificación
                    payloadBase64 = payloadBase64.PadRight(payloadBase64.Length + (4 - payloadBase64.Length % 4) % 4, '=');
                    
                    try 
                    {
                        var payloadBytes = Convert.FromBase64String(payloadBase64);
                        var payloadJson = System.Text.Encoding.UTF8.GetString(payloadBytes);
                        
                        _logger.LogWarning("[DIAGNOSTICO TOKEN] Token Payload JSON: {PayloadJson}", payloadJson);
                        _logger.LogWarning("[DIAGNOSTICO TOKEN] Token obtenido y analizado con éxito.");
                    }
                    catch (FormatException)
                    {
                         _logger.LogError("[DIAGNOSTICO TOKEN] Falló la decodificación Base64 del token.");
                    }
                }
                else
                {
                     _logger.LogWarning("[DIAGNOSTICO TOKEN] Token no tiene formato JWT esperado.");
                }
            }
            
            _logger.LogInformation("Token obtenido de Keycloak para llamada a Stock.");

            // 2. Poner el token en el header de la llamada
            _httpClient.DefaultRequestHeaders.Authorization = 
                new AuthenticationHeaderValue("Bearer", token);

            // 3. Llamar a la API de Stock
            //    La ruta base "productos/" ya está en el BaseAddress.
            var response = await _httpClient.GetAsync($"{product.id}"); 

            var jsonString = await response.Content.ReadAsStringAsync();



            // 4. Si Stock devuelve 401, 403, 500, etc., esto lanzará un error
            if (!response.IsSuccessStatusCode)
            {
                // Incluimos el cuerpo de la respuesta para ver si Stock envía detalles
                var errorBody = await response.Content.ReadAsStringAsync();
                _logger.LogError("Error al llamar a Stock API. Status: {StatusCode}. ProductId: {ProductId}. Respuesta de Stock: {ErrorBody}", 
                                 response.StatusCode, product.id, errorBody);
            }
            response.EnsureSuccessStatusCode(); 


            _logger.LogWarning("[STOCK RESPONSE] JSON Recibido para ID {Id}: {Json}", product.id, jsonString);

            // 5. Leer la respuesta y convertirla de JSON a tu objeto ProductDetail otro puto debería hacer esto cabrón
            using (JsonDocument doc = JsonDocument.Parse(jsonString))
            {
                var root = doc.RootElement;
                var dims = root.GetProperty("dimensiones");
                var productDetail = new ProductDetail
                {
                    id = root.GetProperty("id").GetInt32(),
                    weight = root.GetProperty("pesoKg").GetSingle(),
                    length = dims.GetProperty("largoCm").GetSingle(),
                    width = dims.GetProperty("anchoCm").GetSingle(),
                    height = dims.GetProperty("altoCm").GetSingle()
                };

                _logger.LogInformation("Datos de Stock obtenidos exitosamente para ProductId: {ProductId}", product.id);
                return productDetail;
            }
        }
    }
}