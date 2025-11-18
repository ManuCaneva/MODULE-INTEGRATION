using System.Collections.Generic;
using System.Linq;

namespace ComprasAPI.Models
{
    public class Booking
    {
        public int Id { get; set; }
        public string Status { get; set; }

        public ICollection<BookingProduct> Products { get; set; } = new List<BookingProduct>();
    }
}
