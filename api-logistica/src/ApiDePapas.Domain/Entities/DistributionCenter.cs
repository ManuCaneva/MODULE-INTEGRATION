using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ApiDePapas.Domain.Entities
{
    public class DistributionCenter
        {
            // Clave primaria
            [Required]
            public int distribution_center_id { get; set; } 

            // Referencia a su Objeto de Valor (Address)
            [Required]
            public int address_id { get; set; }
            public Address Address { get; set; } = null!; // Propiedad de navegación
            
    }
}