using ApiDePapas.Domain.Entities;

namespace ApiDePapas.Domain.Repositories
{
    // El repositorio de Shipping hereda las operaciones CRUD básicas
    public interface IShippingRepository : IGenericRepository<ShippingDetail>
    {
        // Operaciones específicas para ShippingDetail
        Task<ShippingDetail?> GetByOrderIdAsync(int orderId);
        Task<IEnumerable<ShippingDetail>> GetByUserIdAsync(int userId);
        
        // Operación para el patrón CQRS/actualización atómica
        Task UpdateStatusAsync(int shippingId, ShippingStatus newStatus);

        IQueryable<ShippingDetail> GetAllQueryable(); // New method for pagination
    }
}