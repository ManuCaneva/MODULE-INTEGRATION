using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ComprasAPI.Data;
using ComprasAPI.Models;
using System.Security.Cryptography;
using System.Text;

namespace ComprasAPI.Controllers
{
    [ApiController]
    [Route("api/auth/register")]
    public class RegisterController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public RegisterController(ApplicationDbContext context)
        {
            _context = context;
        }

        [HttpPost]
        public async Task<IActionResult> Register(RegisterRequest request)
        {
            if (request.Password != request.RepeatPassword)
                return BadRequest("Las contraseñas no coinciden.");

            if (await _context.Users.AnyAsync(u => u.Email == request.Email))
                return BadRequest("El correo ya está registrado.");

            var user = new User
            {
                FirstName = request.FirstName,
                LastName = request.LastName,
                Email = request.Email,
                PasswordHash = HashPassword(request.Password),
                CreatedAt = DateTime.Now
            };

            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            return Ok("Usuario registrado correctamente.");
        }

        private string HashPassword(string password)
        {
            using var sha256 = SHA256.Create();
            var bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));
            return Convert.ToBase64String(bytes);
        }
    }
}