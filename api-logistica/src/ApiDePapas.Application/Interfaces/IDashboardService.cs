using System.Collections.Generic;
using System.Threading.Tasks;
using ApiDePapas.Application.DTOs;

namespace ApiDePapas.Application.Interfaces
{
    public interface IDashboardService
    {
        Task<IEnumerable<DashboardShipmentDto>> GetDashboardShipmentsAsync(int page, int pageSize);
        Task<int> GetTotalDashboardShipmentsCountAsync();
    }
}
