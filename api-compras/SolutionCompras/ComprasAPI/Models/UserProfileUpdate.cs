namespace ComprasAPI.Models
{
    public class UserProfileUpdate
    {
        public string Phone { get; set; } = string.Empty;
        public string Dni { get; set; } = string.Empty;
        public DateTime BirthDate { get; set; }
    }
}
