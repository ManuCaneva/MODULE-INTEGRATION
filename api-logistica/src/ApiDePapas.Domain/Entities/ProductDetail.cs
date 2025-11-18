using System.ComponentModel.DataAnnotations;
using System.Numerics;

//Hay que cambiar la estructura para que sea acorde a lo que nos da stock. address, etc.

namespace ApiDePapas.Domain.Entities
{
    public class ProductDetail
    {
        [Required]
        public int id { get; set; }

        [Required]
        public float weight { get; set; }

        [Required]
        public float length { get; set; }

        [Required]
        public float width { get; set; }

        [Required]
        public float height { get; set; }
    }
}