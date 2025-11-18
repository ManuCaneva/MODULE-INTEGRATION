namespace ComprasAPI.Models
{
    public class Order
    {
        public int Id { get; set; }
        public DateTime Date { get; set; }
        public string Status { get; set; }
        public ICollection<CartItem> Items { get; set; } = new List<CartItem>();
        public decimal Total { get; set; }

        public int UserId { get; set; }

    }
}
