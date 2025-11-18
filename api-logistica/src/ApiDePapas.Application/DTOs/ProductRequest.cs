using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ApiDePapas.Application.DTOs
{
    public record ProductRequest(
        [property: JsonPropertyName("id")]
        [Required]
        int id,

        [property: JsonPropertyName("quantity")]
        [Required]
        [Range(1, int.MaxValue, ErrorMessage = "Quantity must be at least 1")]
        int quantity
    );
}