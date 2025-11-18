using ComprasAPI.Data;
using ComprasAPI.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System;
using System.Security.Claims;

namespace ComprasAPI.Controllers
{
    [ApiController]
    [Route("api/user/profile")]
    [Authorize]
    public class UserProfileController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public UserProfileController(ApplicationDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<IActionResult> GetUserProfile()
        {
            try
            {
                var userEmail = GetUserEmailFromToken();
                if (string.IsNullOrEmpty(userEmail))
                    return Unauthorized(new { error = "No autorizado" });

                var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == userEmail);
                if (user == null)
                    return NotFound(new { error = "Usuario no encontrado" });

                var profile = await _context.UserProfiles.FirstOrDefaultAsync(p => p.UserId == user.Id);
                if (profile == null)
                    return NotFound(new { error = "Perfil no encontrado" });

                return Ok(profile);
            }
            catch (Exception)
            {
                return StatusCode(500, new { error = "Error interno del servidor" });
            }
        }

        [HttpPost]
        public async Task<IActionResult> CreateUserProfile([FromBody] UserProfileCreate request)
        {
            try
            {
                var userEmail = GetUserEmailFromToken();
                if (string.IsNullOrEmpty(userEmail))
                    return Unauthorized(new { error = "No autorizado" });

                var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == userEmail);
                if (user == null)
                    return Unauthorized(new { error = "Usuario no encontrado" });

                var existingProfile = await _context.UserProfiles.FirstOrDefaultAsync(p => p.UserId == user.Id);
                if (existingProfile != null)
                    return Conflict(new { error = "El perfil ya existe" });

                var dniExists = await _context.UserProfiles.AnyAsync(p => p.Dni == request.Dni);
                if (dniExists)
                    return Conflict(new { error = "El DNI ya está registrado" });

                var profile = new UserProfile
                {
                    UserId = user.Id,
                    Phone = request.Phone,
                    Dni = request.Dni,
                    BirthDate = request.BirthDate,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                };

                _context.UserProfiles.Add(profile);
                await _context.SaveChangesAsync();

                return Created("", new { message = "Perfil creado exitosamente" });
            }
            catch (Exception)
            {
                return StatusCode(500, new { error = "Error interno del servidor" });
            }
        }

        [HttpPut]
        public async Task<IActionResult> UpdateUserProfile([FromBody] UserProfileUpdate request)
        {
            try
            {
                var userEmail = GetUserEmailFromToken();
                if (string.IsNullOrEmpty(userEmail))
                    return Unauthorized(new { error = "No autorizado" });

                var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == userEmail);
                if (user == null)
                    return Unauthorized(new { error = "Usuario no encontrado" });

                var profile = await _context.UserProfiles.FirstOrDefaultAsync(p => p.UserId == user.Id);
                if (profile == null)
                    return NotFound(new { error = "Perfil no encontrado" });

                var dniExists = await _context.UserProfiles.AnyAsync(p => p.Dni == request.Dni && p.UserId != user.Id);
                if (dniExists)
                    return Conflict(new { error = "El DNI ya está registrado" });

                profile.Phone = request.Phone;
                profile.Dni = request.Dni;
                profile.BirthDate = request.BirthDate;
                profile.UpdatedAt = DateTime.UtcNow;

                await _context.SaveChangesAsync();

                return Ok(new { message = "Perfil actualizado exitosamente" });
            }
            catch (Exception)
            {
                return StatusCode(500, new { error = "Error interno del servidor" });
            }
        }

        private string? GetUserEmailFromToken()
        {
            var emailClaim = User.FindFirst(ClaimTypes.Name) ?? User.FindFirst(ClaimTypes.NameIdentifier);
            return emailClaim?.Value;
        }
    }
}
