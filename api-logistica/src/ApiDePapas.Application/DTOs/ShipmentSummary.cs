using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

using ApiDePapas.Domain.Entities;

namespace ApiDePapas.Application.DTOs
{
    // Representa el resumen de un envío en una lista.
    public record ShipmentSummary(
        [property: JsonPropertyName("shipping_id")]
        [Required]
        int ShippingId,

        [property: JsonPropertyName("order_id")]
        [Required]
        int OrderId,

        [property: JsonPropertyName("user_id")]
        [Required]
        int UserId,

        [property: JsonPropertyName("products")]
        [Required]
        List<ProductQty> Products,

        [property: JsonPropertyName("status")]
        [Required]
        ShippingStatus Status,

        [property: JsonPropertyName("transport_type")]
        [Required]
        TransportType TransportType,

        [property: JsonPropertyName("estimated_delivery_at")]
        [Required]
        DateTime EstimatedDeliveryAt,

        [property: JsonPropertyName("created_at")]
        [Required]
        DateTime CreatedAt
    );
}
