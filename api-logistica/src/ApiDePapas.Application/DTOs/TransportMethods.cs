using System.ComponentModel.DataAnnotations;

using ApiDePapas.Domain.Entities;

namespace ApiDePapas.Application.DTOs
{
    public class TransportMethods
    {
        public TransportType type { get; set; }

        public string name { get; set; } = string.Empty;

        public string estimated_days { get; set; } = string.Empty;
    }
} 
