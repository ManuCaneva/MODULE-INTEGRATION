namespace ComprasAPI.Models
{
    public class Tracking
    {
        public int Id { get; set; }
        public string Status { get; set; }
        public int OrderId { get; set; }
        public DateTime CreationDate { get; set; }
    }
}
