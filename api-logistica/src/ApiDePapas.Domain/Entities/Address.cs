using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;
using System.Collections.Generic; // Necesario para la colección de navegación inversa

namespace ApiDePapas.Domain.Entities
{
    // Usamos 'class' porque ahora es una Entidad de DB con su propia PK
    public class Address
    {
        // 1. CLAVE PRIMARIA (PK) para la tabla 'Addresses'
        [Required]
        [Key]
        public int address_id { get; set; } // Identificador único de la dirección

        // 2. PROPIEDADES FÍSICAS
        [property: JsonPropertyName("street")]
        [Required]
        public string street { get; set; } = string.Empty;

        [property: JsonPropertyName("number")]
        // Cambié a 'string' para mayor flexibilidad, pero 'int' también es válido si se ajustan los setters
        public int number { get; set; } = 0; 

        // 3. CLAVES FORÁNEAS (FK) a Locality (clave compuesta)
        // Estos campos se usan para un JOIN a la tabla Locality
        [property: JsonPropertyName("postal_code")]
        [Required]
        public string postal_code { get; set; } = string.Empty;

        [property: JsonPropertyName("locality_name")]
        [Required]
        public string locality_name { get; set; } = string.Empty;


        // 4. PROPIEDAD DE NAVEGACIÓN (hacia la entidad Locality)
        // Permite cargar los datos completos de la localidad.
        public Locality Locality { get; set; } = null!;
        
        // 5. PROPIEDAD DE NAVEGACIÓN INVERSA (hacia ShippingDetail)
        // Se usa para las direcciones de entrega (DeliveredShippings)
        public ICollection<ShippingDetail> DeliveredShippings { get; set; } = new List<ShippingDetail>();
    }
}