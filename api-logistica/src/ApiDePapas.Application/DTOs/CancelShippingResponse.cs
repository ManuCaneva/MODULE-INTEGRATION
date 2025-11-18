using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

using ApiDePapas.Domain.Entities;

namespace ApiDePapas.Application.DTOs
{
    public record CancelShippingResponse(
        [property: JsonPropertyName("shipping_id")]
        [Required]
        int shipping_id,

        [property: JsonPropertyName("status")]
        [Required]
        ShippingStatus status,

        [property: JsonPropertyName("cancelled_at")]
        [Required]
        DateTime cancelled_at
    );
}
