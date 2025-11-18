using System.Threading.Tasks;
using ApiDePapas.Domain.Entities;

namespace ApiDePapas.Application.Interfaces
{
    public interface IStockService
    {
        Task<ProductDetail> GetProductDetailAsync(ProductQty product);
    }
}