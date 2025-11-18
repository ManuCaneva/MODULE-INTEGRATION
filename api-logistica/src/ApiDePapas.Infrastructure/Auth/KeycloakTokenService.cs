using ApiDePapas.Application.Interfaces;
using Microsoft.Extensions.Configuration;
using System.Net.Http;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Text.Json;
using System; // Agregado para usar DateTime

namespace ApiDePapas.Infrastructure.Auth
{
    /**
     * Servicio para obtener un Access Token de Keycloak
     * usando Client Credentials.
     */
    public class KeycloakTokenService : ITokenService
    {
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly IConfiguration _configuration;
        private string _cachedToken;
        private DateTime _tokenExpiresAt;

        public KeycloakTokenService(IHttpClientFactory httpClientFactory, IConfiguration configuration)
        {
            _httpClientFactory = httpClientFactory;
            _configuration = configuration;
            _tokenExpiresAt = DateTime.UtcNow;
        }

        public async Task<string> GetAccessTokenAsync()
        {
            // Revisa si el token cacheado es válido (con un margen de 30s)
            if (!string.IsNullOrEmpty(_cachedToken) && _tokenExpiresAt > DateTime.UtcNow.AddSeconds(30))
            {
                return _cachedToken;
            }

            // Si no, pide uno nuevo
            var client = _httpClientFactory.CreateClient("KeycloakClient");
            
            var tokenEndpoint = _configuration["Keycloak:TokenEndpoint"];
            var clientId = _configuration["Keycloak:ClientId"];
            var clientSecret = _configuration["Keycloak:ClientSecret"];
            
            // 💡 CORRECCIÓN CLAVE: Agregando el scope requerido por la API de Stock
            // El Scope 'openid' siempre debe ser incluido. Añadimos 'productos:read'
            // ya que Logística necesita leer datos de Stock (ProductosController).
            const string requiredScopes = "openid productos:read"; 
            
            var content = new FormUrlEncodedContent(new[]
            {
                new KeyValuePair<string, string>("grant_type", "client_credentials"),
                new KeyValuePair<string, string>("client_id", clientId),
                new KeyValuePair<string, string>("client_secret", clientSecret),
                // 💡 AGREGADO: Incluimos el parámetro scope en la solicitud
                new KeyValuePair<string, string>("scope", requiredScopes) 
            });

            var response = await client.PostAsync(tokenEndpoint, content);

            if (!response.IsSuccessStatusCode)
            {
                // Incluir más detalles sobre el error para un mejor diagnóstico futuro
                var errorContent = await response.Content.ReadAsStringAsync();
                throw new ApplicationException($"No se pudo obtener el token de Keycloak. Status: {response.StatusCode}. Detalle: {errorContent}");
            }

            var responseString = await response.Content.ReadAsStringAsync();
            
            // Usamos un objeto simple para deserializar en lugar de JsonDocument para mayor robustez
            var tokenResponse = JsonSerializer.Deserialize<KeycloakTokenResponse>(responseString);

            _cachedToken = tokenResponse.access_token;
            _tokenExpiresAt = DateTime.UtcNow.AddSeconds(tokenResponse.expires_in);

            return _cachedToken;
        }
    }

    // Clase auxiliar para deserializar la respuesta del token
    public class KeycloakTokenResponse
    {
        public string access_token { get; set; }
        public int expires_in { get; set; }
        public int refresh_expires_in { get; set; }
        public string token_type { get; set; }
        public string session_state { get; set; }
        public string scope { get; set; }
    }
}