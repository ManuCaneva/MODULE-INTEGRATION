namespace ComprasAPI.Models
{
    public class User
    {
        public int Id { get; set; }                     // Primary Key (PK)
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Email { get; set; }
        public string PasswordHash { get; set; }
        public DateTime CreatedAt { get; set; } = DateTime.Now;

        //Relación 1:1 con UserProfile
        public UserProfile UserProfile { get; set; }
    }
}
