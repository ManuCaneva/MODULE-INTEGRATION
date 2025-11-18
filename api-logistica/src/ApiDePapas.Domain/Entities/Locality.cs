using System.ComponentModel.DataAnnotations;

namespace ApiDePapas.Domain.Entities
{
    public class Locality
    {
        // Usaremos el código postal como clave primaria o identificador
        [Required]
        [Key] // Indicamos que este será el campo clave en la BD'
        [RegularExpression(@"^([A-Z]{1}\d{4}[A-Z]{3})$", ErrorMessage = "Invalid postal code format")]
        public string postal_code { get; set; } = string.Empty; 

        [Required]
        public string locality_name { get; set; } = string.Empty;

        [Required]
        public string state_name { get; set; } = string.Empty;

        [Required]
        public string country { get; set; } = string.Empty;

        [Required]
        public float lat { get; set; } // O double, según tu precisión
        
        [Required]
        public float lon { get; set; } // O double
    }
}