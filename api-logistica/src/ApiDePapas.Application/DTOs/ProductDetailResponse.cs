using System.Text.Json.Serialization;

namespace ApiDePapas.Application.DTOs
{
    public class ProductDetailResponse
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }

        [JsonPropertyName("weight")]
        public float Weight { get; set; }

        [JsonPropertyName("length")]
        public float Length { get; set; }

        [JsonPropertyName("width")]
        public float Width { get; set; }

        [JsonPropertyName("height")]
        public float Height { get; set; }

        // Nuevo campo agregado para mejorar el calculo
        // permite nulo porque no era parte del contrato original
        [JsonPropertyName("warehouse_postal_code")]
        public string? WarehousePostalCode { get; set; }
    }
}