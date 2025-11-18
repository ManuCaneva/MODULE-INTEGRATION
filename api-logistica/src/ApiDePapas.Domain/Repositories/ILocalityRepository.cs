// En src/ApiDePapas.Domain/Repositories/ILocalityRepository.cs
using ApiDePapas.Domain.Entities;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace ApiDePapas.Domain.Repositories
{
    public interface ILocalityRepository : IGenericRepository<Locality>
    {
        Task<Locality?> GetByCompositeKeyAsync(string postalCode, string localityName);

        // Mantenemos la funcionalidad de búsqueda flexible (de la rama VIEJA)
        Task<IEnumerable<Locality>> SearchAsync(
            string? state = null,
            string? localityName = null,
            string? postalCode = null,
            int page = 1,
            int limit = 50);

        // Mantenemos la funcionalidad nueva (de la rama ACTUAL)
        Task<List<Locality>> GetByPostalCodeAsync(string postalCode);
    }
}