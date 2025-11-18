using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using ApiDePapas.Application.Interfaces;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace ApiDePapas.Application.Services
{
    public class PurchasingService : IPurchasingService
    {
        private readonly HttpClient _httpClient;
        private readonly string _purchasingApiUrl;
        private readonly ILogger<PurchasingService> _logger;

        public PurchasingService(HttpClient httpClient, IConfiguration configuration, ILogger<PurchasingService> logger)
        {
            _httpClient = httpClient;
            _purchasingApiUrl = configuration["ExternalApi:PurchasingUrl"];
            _logger = logger;
        }

        public async Task NotifyShippingCancellationAsync(int shippingId)
        {
            try
            {
                var requestBody = new { shipping_id = shippingId };
                var jsonBody = JsonSerializer.Serialize(requestBody);
                var content = new StringContent(jsonBody, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync($"{_purchasingApiUrl}/api/cancellation", content);

                if (!response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    _logger.LogError("Error notifying purchasing service about cancellation for shipping ID {ShippingId}. Status: {StatusCode}, Response: {Response}", shippingId, response.StatusCode, responseContent);
                    // We are not throwing an exception here because the cancellation of the shipping in our system was successful.
                    // We just log the error from the notification. A more robust system could use a retry mechanism or an outbox pattern.
                }
                
                response.EnsureSuccessStatusCode();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "An unexpected error occurred while notifying purchasing service for shipping ID {ShippingId}.", shippingId);
                // As above, we don't re-throw the exception.
            }
        }
    }
}
