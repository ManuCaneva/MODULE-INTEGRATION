using System.Collections.Generic;
using ApiDePapas.Domain.Entities;
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ApiDePapas.Application.DTOs
{
    // Define el DTO de la Dirección de ENTRADA
    public record DeliveryAddressRequest(
        [property: JsonPropertyName("street")]
        [Required]
        string street = "",

        [property: JsonPropertyName("number")]
        [Required]
        int number = 0,

        [property: JsonPropertyName("postal_code")]
        [Required]
        string postal_code = "",

        [property: JsonPropertyName("locality_name")]
        [Required]
        string locality_name = ""
    );
}