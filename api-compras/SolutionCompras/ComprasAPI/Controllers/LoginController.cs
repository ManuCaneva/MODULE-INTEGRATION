using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ComprasAPI.Data;
using ComprasAPI.Models;
using System.Security.Cryptography;
using System.Text;

namespace ComprasAPI.Controllers
{
    [ApiController]
    [Route("api/auth/login")]
    public class LoginController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public LoginController(ApplicationDbContext context)
        {
            _context = context;
        }

        [HttpPost]
        public async Task<IActionResult> Login(LoginRequest request)
        {
            var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == request.Email);
            if (user == null)
                return Unauthorized("Usuario no encontrado.");

            if (user.PasswordHash != HashPassword(request.Password))
                return Unauthorized("Contraseña incorrecta.");

            return Ok("Inicio de sesión exitoso.");
        }

        private string HashPassword(string password)
        {
            using var sha256 = SHA256.Create();
            var bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));
            return Convert.ToBase64String(bytes);
        }
    }
}