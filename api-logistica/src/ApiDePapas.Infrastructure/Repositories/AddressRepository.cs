using ApiDePapas.Domain.Entities;
using ApiDePapas.Domain.Repositories;
using ApiDePapas.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;
using System.Linq.Expressions;

namespace ApiDePapas.Infrastructure.Repositories
{
    public class AddressRepository : IAddressRepository
    {
        private readonly ApplicationDbContext _context;

        public AddressRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        // Método específico para buscar una dirección existente
        public async Task<Address?> FindExistingAddressAsync(string street, int number, string postalCode, string localityName)
        {
            return await _context.Addresses
                .FirstOrDefaultAsync(a => 
                    a.street == street && 
                    a.number == number &&
                    a.postal_code == postalCode &&
                    a.locality_name == localityName);
        }

        // Implementación de IGenericRepository<Address>
        public async Task AddAsync(Address entity)
        {
            await _context.Addresses.AddAsync(entity);
            await _context.SaveChangesAsync();
        }

        // Nota: Debes implementar los demás métodos CRUD de IGenericRepository aquí (GetAllAsync, GetByIdAsync, etc.)
        public Task<IEnumerable<Address>> GetAllAsync() => throw new NotImplementedException();
        public Task<Address?> GetByIdAsync(int id) => throw new NotImplementedException();
        public void Update(Address entity) => throw new NotImplementedException();
        public void Delete(Address entity) => throw new NotImplementedException();
        public Task<IEnumerable<Address>> FindAsync(Expression<Func<Address, bool>> predicate) => throw new NotImplementedException();
        public Task<bool> ExistsAsync(Expression<Func<Address, bool>> predicate) => throw new NotImplementedException();
    }
}