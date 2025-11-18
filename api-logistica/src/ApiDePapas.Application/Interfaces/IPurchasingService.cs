using System.Threading.Tasks;

namespace ApiDePapas.Application.Interfaces
{
    public interface IPurchasingService
    {
        Task NotifyShippingCancellationAsync(int shippingId);
    }
}
