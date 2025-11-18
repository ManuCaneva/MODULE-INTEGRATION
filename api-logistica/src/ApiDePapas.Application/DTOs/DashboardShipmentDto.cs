
using System;
using System.Collections.Generic;
using ApiDePapas.Domain.Entities;

namespace ApiDePapas.Application.DTOs
{
    public class DashboardShipmentDto
    {
        public int shipping_id { get; set; }
        public int order_id { get; set; }
        public int user_id { get; set; }
        public List<ProductQty> products { get; set; } = new List<ProductQty>();
        public ShippingStatus status { get; set; }
        public TransportType transport_type { get; set; }
        public DateTime estimated_delivery_at { get; set; }
        public DateTime created_at { get; set; }
        public AddressReadDto delivery_address { get; set; } = new AddressReadDto();
        public AddressReadDto departure_address { get; set; } = new AddressReadDto();
    }
}
