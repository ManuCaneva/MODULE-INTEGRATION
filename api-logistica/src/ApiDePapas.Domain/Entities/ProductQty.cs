using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

//Se usa en ShippingDetails

namespace ApiDePapas.Domain.Entities
{
    // Modelo de SALIDA (Detalle): Representa un producto dentro de un envío ya creado.
    public record ProductQty(

        // lo siguiente es id del producto, lo sacamos de stock y lo guardamos (relacionamos con el id del shipping)
        [property: JsonPropertyName("product_id")]
        [Required]
        int id,

        [property: JsonPropertyName("quantity")]
        [Required]
        [Range(1, int.MaxValue)]
        int quantity
    );
}
