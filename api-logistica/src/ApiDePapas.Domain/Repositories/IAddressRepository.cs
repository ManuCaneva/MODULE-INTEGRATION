using ApiDePapas.Domain.Entities;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace ApiDePapas.Domain.Repositories
{
    // Usaremos esta interfaz para crear nuevas direcciones si no existen
    public interface IAddressRepository : IGenericRepository<Address>
    {
        // Método para buscar una dirección por sus campos físicos (calle, número, FKs)
        Task<Address?> FindExistingAddressAsync(string street, int number, string postalCode, string localityName);
    }
}