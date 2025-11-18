using System.Collections.Generic;
using System.Linq;

namespace ComprasAPI.Models
{
    public class Cart
    {
        public int Id { get; set; }
        public ICollection<CartItem> Items { get; set; } = new List<CartItem>();
        public decimal Total { get; set; }

        public int UserId { get; set; }  // quién es dueño del carrito
    }
}
