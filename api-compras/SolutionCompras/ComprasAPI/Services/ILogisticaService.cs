using ComprasAPI.Models.DTOs;

namespace ComprasAPI.Services
{
    public interface ILogisticaService
    {
        Task<ShippingCostResponse> CalcularCostoEnvioAsync(ShippingCostRequest request);
        Task<CreateShippingResponse> CrearEnvioAsync(CreateShippingRequest request);
        Task<ShippingDetail> ObtenerSeguimientoAsync(int shippingId);
        Task<List<TransportMethod>> ObtenerMetodosTransporteAsync();
        Task<bool> CancelarEnvioAsync(int shippingId);
        //Task<object> ObtenerEnviosFiltradosAsync(int? userId, string? status, DateTime? fromDate, DateTime? toDate, int page, int limit);

    }


}