using ApiDePapas.Domain.Entities;
using ApiDePapas.Application.Interfaces;
using ApiDePapas.Application.DTOs;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Threading.Tasks;

/* 
 * Quotes cost for a shipment without creating any resources.
 * Used by Order Management module to show shipping options to customers before purchase.
 *
 * Integration Flow:
 * 1. Order Management sends only: delivery_address + product IDs with quantities
 * 2. Logistics queries Stock module for EACH product:
 *    - GET /products/{id} → returns weight, dimensions, warehouse_postal_code
 * 3. Logistics calculates:
 *    - Total weight = sum(product.weight * quantity)
 *    - Total volume = sum(product dimensions * quantity)
 *    - Distance = from warehouse_postal_code to delivery_address.postal_code
 * 4. Returns estimated cost based on weight, volume, distance, and transport type
 * 5. NO data is persisted (quote only)
 */

/*
 * Se tiene que tener en cuenta el medio de transporte para calcular el precio?
 * Como se determina qué medio de transporse se utiliza?
 */

namespace ApiDePapas.Application.Services
{
    public class CalculateCost : ICalculateCost
    {
        private readonly IStockService _stockService;
        private readonly IDistanceService _distance;
        // como no tenemos un servicio de distancia, usamos uno en memoria
        private const string DEFAULT_ORIGIN_CPA = "H3500";

        public CalculateCost(IStockService stockService, IDistanceService distance)
        {
            _stockService = stockService;
            _distance = distance;
        }
        public async Task<ShippingCostResponse> CalculateShippingCostAsync(ShippingCostRequest request)
        {
            float total_cost = 0f;
            List<ProductOutput> products_with_cost = new List<ProductOutput>();

            // Distancia base: de un CD por defecto al destino
            // (Cuando Stock empiece a devolver warehouse_postal_code por producto, lo usamos ahí)
            var distance_km_request = (float)await _distance.GetDistanceKm(DEFAULT_ORIGIN_CPA, request.delivery_address.postal_code);

            foreach (var prod in request.products)
            {
                //Si usamos api real de stock, esto va a ser una llamada HTTP
                //DistanceServiceExternal : IDistanceService (HTTP → geocoding).
                //En FakeStockService/Stock real, devolver warehouse_postal_code en ProductDetail.
                //aqui dentro del FOREACH DEBE CAMBIAR:
                //var origin = prod_detail.warehouse_postal_code ?? DEFAULT_ORIGIN_CPA;
                //float distance_km = (float)_distance.GetDistanceKm(origin, request.delivery_address.postal_code);

                ProductDetail prod_detail = await _stockService.GetProductDetailAsync(prod);

                float total_weight_grs = prod_detail.weight * prod.quantity;

                float prod_volume_cm3 = prod_detail.length * prod_detail.width * prod_detail.height;
                float total_volume = prod_volume_cm3 * prod.quantity;

                
                // float distance_km = _CalculateDistance(request.delivery_address.postal_code, prod_detail.postal_code);
                float distance_km =distance_km_request;

                // Calcular costo, formula de ejemplo
                float partial_cost = total_weight_grs * 1.2f + prod_volume_cm3 * 0.5f + distance_km * 8.0f;

                total_cost += partial_cost;

                products_with_cost.Add(new ProductOutput(prod.id, partial_cost));
            }

            var response = new ShippingCostResponse("ARS", total_cost, TransportType.plane, products_with_cost);

            return response;
        }
    }
}
