namespace ComprasAPI.Models
{
    public class BookingProduct
    {
        public int Id { get; set; }
        public int BookingId { get; set; }
        public int ProductId { get; set; }
        public int Quantity { get; set; }

        public Booking Booking { get; set; }
    }
}
