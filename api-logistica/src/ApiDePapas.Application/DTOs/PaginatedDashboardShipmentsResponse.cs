using System.Collections.Generic;

namespace ApiDePapas.Application.DTOs
{
    public record PaginatedDashboardShipmentsResponse(
        IEnumerable<DashboardShipmentDto> shipments,
        PaginationData pagination
    );
}
