using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace ComprasAPI.Models.DTOs
{
    // --- DTOs DE PETICIÓN (REQUESTS) ---

    // Request para calcular costo de envío
    public class ShippingCostRequest
    {
        [JsonPropertyName("delivery_address")] // Mapea a snake_case para Logística
        public Address DeliveryAddress { get; set; }

        [JsonPropertyName("products")]
        public List<ProductRequest> Products { get; set; }
    }

    // Request para crear envío
    public class CreateShippingRequest
    {
        public int OrderId { get; set; }
        public int UserId { get; set; }
        public Address DeliveryAddress { get; set; }
        public string TransportType { get; set; }
        public List<ProductRequest> Products { get; set; }
    }

    // --- DTOs DE RESPUESTA (RESPONSES) ---

    // Response de cálculo de costo
    public class ShippingCostResponse
    {
        /*public string Currency { get; set; }
        public decimal TotalCost { get; set; }
        public string TransportType { get; set; }
        public List<ProductCost> Products { get; set; }
        */
        [JsonPropertyName("currency")]
        public string Currency { get; set; }
        [JsonPropertyName("total_cost")]
        public decimal TotalCost { get; set; }
        [JsonPropertyName("transport_type")] 
        public string TransportType { get; set; } 
        [JsonPropertyName("products")]
        public List<ProductCost> Products { get; set; }
    }

    // Response de creación de envío
    public class CreateShippingResponse
    {
        public int ShippingId { get; set; }
        public string Status { get; set; }
        public string TransportType { get; set; }
        public string EstimatedDeliveryAt { get; set; }
    }

    // Detalle de seguimiento
    public class ShippingDetail
    {
        public int ShippingId { get; set; }
        public string Status { get; set; }
        public string EstimatedDeliveryAt { get; set; }
        public string TrackingNumber { get; set; }
        public string CarrierName { get; set; }
    }

    // Métodos de transporte
    public class TransportMethodsResponse
    {
        public List<TransportMethod> TransportMethods { get; set; }
    }

    // --- OBJETOS AUXILIARES ---

    public class TransportMethod
    {
        public string Type { get; set; }
        public string Name { get; set; }
        public string EstimatedDays { get; set; }
    }

    public class Address
    {
        [JsonPropertyName("street")]
        public string Street { get; set; }

        // Mapeamos tu "City" para que viaje como "locality_name"
        [JsonPropertyName("locality_name")] 
        public string City { get; set; }

        // Logística EXIGE este campo numérico separado.
        [JsonPropertyName("number")]
        public int Number { get; set; } 

        [JsonPropertyName("postal_code")]
        public string PostalCode { get; set; }

        // Estos campos no son obligatorios para el cálculo, pero los dejamos
        public string State { get; set; }
        public string Country { get; set; }
    }

    public class ProductRequest
    {
        [JsonPropertyName("product_id")] // Mapea 'Id' a 'product_id'
        public int Id { get; set; }

        [JsonPropertyName("quantity")]
        public int Quantity { get; set; }
    }

    public class ProductCost
    {
        public int Id { get; set; }
        public decimal Cost { get; set; }
    }
}