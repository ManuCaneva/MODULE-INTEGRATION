namespace ComprasAPI.Models
{
    public class UserProfileCreate
    {
        public string Phone { get; set; } = string.Empty;
        public string Dni { get; set; } = string.Empty;
        public DateTime BirthDate { get; set; }
    }
}
