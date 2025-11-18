using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ApiDePapas.Application.DTOs
{
    // Contiene la metadata para las respuestas paginadas.
    public record PaginationData(
        [property: JsonPropertyName("current_page")]
        [Required]
        int current_page,

        [property: JsonPropertyName("total_pages")]
        [Required]
        int total_pages,

        [property: JsonPropertyName("total_items")]
        [Required]
        int total_items,

        [property: JsonPropertyName("items_per_page")]
        [Required]
        int items_per_page
    );
}