using ApiDePapas.Domain.Entities; 
using System.Collections.Generic;
using System.Text.Json.Serialization;
using System;
using System.Linq;

namespace ApiDePapas.Application.DTOs
{
    // DTOs Anidados para Romper el Ciclo JSON y exponer solo lo necesario
    
    // DTO para la ADDRESS (Reemplaza $ref: "#/components/schemas/Address")
    // Nota: Usaremos este DTO para mapear delivery_address y departure_address
    public class AddressReadDto
    {
        public int address_id { get; set; }
        public string street { get; set; } = string.Empty;
        public int number { get; set; }
        public string postal_code { get; set; } = string.Empty;
        public string locality_name { get; set; } = string.Empty;
        // Aquí podrías agregar más campos de Locality si son esenciales, ej: state_name
    }

    public class TransportMethodReadDto
    {
        public int transport_id { get; set; }
        public string transport_type { get; set; } = string.Empty;
        // Solo las propiedades básicas del transporte
    }
    
    public record ProductQtyReadDto(
        [property: JsonPropertyName("product_id")] int product_id, 
        [property: JsonPropertyName("quantity")] int quantity
    );
    public record ShippingLogReadDto(DateTime timestamp, ShippingStatus status, string message);


    // DTO FINAL: ShippingDetailResponse (Coincide con el esquema ShippingDetail del YAML)
public class ShippingDetailResponse
    {
        // =================================================================
        // GRUPO 1: Identificación y FKs (Orden 1 a 3)
        // =================================================================
        [JsonPropertyOrder(1)] public int shipping_id { get; set; }
        [JsonPropertyOrder(2)] public int order_id { get; set; }
        [JsonPropertyOrder(3)] public int user_id { get; set; }

        // =================================================================
        // GRUPO 2: Direcciones (Orden 4 y 5)
        // =================================================================
        [JsonPropertyOrder(4)] public AddressReadDto delivery_address { get; set; } = new AddressReadDto();
        [JsonPropertyOrder(5)] public AddressReadDto departure_address { get; set; } = new AddressReadDto(); 
        
        // =================================================================
        // GRUPO 3: Colecciones y Status (Orden 6 a 8)
        // =================================================================
        [JsonPropertyOrder(6)] public List<ProductQtyReadDto> products { get; set; } = new List<ProductQtyReadDto>();
        [JsonPropertyOrder(7)] public ShippingStatus status { get; set; }
        [JsonPropertyOrder(8)] public string transport_type { get; set; } = string.Empty; 

        // =================================================================
        // GRUPO 4: Detalles (Orden 9 a 12)
        // =================================================================
        [JsonPropertyOrder(9)] public string tracking_number { get; set; } = string.Empty;
        [JsonPropertyOrder(10)] public string carrier_name { get; set; } = string.Empty;
        [JsonPropertyOrder(11)] public float total_cost { get; set; }
        [JsonPropertyOrder(12)] public string currency { get; set; } = string.Empty;

        // =================================================================
        // GRUPO 5: Fechas (Orden 13 a 16)
        // =================================================================
        [JsonPropertyOrder(13)] public DateTime estimated_delivery_at { get; set; }
        [JsonPropertyOrder(14)] public DateTime created_at { get; set; }
        [JsonPropertyOrder(15)] public DateTime updated_at { get; set; }
        [JsonPropertyOrder(16)] public List<ShippingLogReadDto> logs { get; set; } = new List<ShippingLogReadDto>();
    }
}