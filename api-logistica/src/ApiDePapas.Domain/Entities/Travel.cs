using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;

namespace ApiDePapas.Domain.Entities
{
    public class Travel
    {
        [Required]
        public int travel_id { get; set; } // Clave primaria del viaje

        [Required]
        public DateTime departure_time { get; set; } // Hora de inicio del viaje

        public DateTime? arrival_time { get; set; } // Hora de llegada (opcional, puede ser nulo)

        // 1. Clave Foránea al Transporte (el camión)
        [Required]
        public int transport_method_id { get; set; }
        public TransportMethod TransportMethod { get; set; } = null!; // Propiedad de navegación

        // 2. Clave Foránea al Centro de Distribución (Origen o Destino)
        [Required]
        public int distribution_center_id { get; set; }
        public DistributionCenter DistributionCenter { get; set; } = null!; // Propiedad de navegación
        
        // 3. Colección de Envíos asociados a este viaje
        public ICollection<ShippingDetail> Shippings { get; set; } = new List<ShippingDetail>();
    }
}