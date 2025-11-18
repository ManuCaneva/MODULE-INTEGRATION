using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

using ApiDePapas.Domain.Entities;

namespace ApiDePapas.Application.DTOs
{
    public record CreateShippingResponse(
        [property: JsonPropertyName("shipping_id")]
        [Required]
        int shipping_id,

        [property: JsonPropertyName("status")]
        [Required]
        ShippingStatus status,

        [property: JsonPropertyName("transport_type")]
        [Required]
        TransportType transport_type,

        [property: JsonPropertyName("estimated_delivery_at")]
        [Required]
        DateTime estimated_delivery_at
    );
}