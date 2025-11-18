using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

using ApiDePapas.Domain.Entities;

namespace ApiDePapas.Application.DTOs
{
    public record CreateShippingRequest(
        [property: JsonPropertyName("order_id")]
        [Required]
        int order_id,

        [property: JsonPropertyName("user_id")]
        [Required]
        int user_id,

        [property: JsonPropertyName("delivery_address")]
        [Required]
        DeliveryAddressRequest delivery_address,

        [property: JsonPropertyName("transport_type")]
        [Required]
        TransportType transport_type,

        [property: JsonPropertyName("products")]
        [Required]
        List<ProductRequest> products
    );
}