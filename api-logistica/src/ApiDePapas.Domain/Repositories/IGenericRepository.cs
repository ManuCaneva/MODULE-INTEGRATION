using System.Linq.Expressions;

namespace ApiDePapas.Domain.Repositories
{
    public interface IGenericRepository<T> where T : class
    {
        // CRUD Básico
        Task<IEnumerable<T>> GetAllAsync();
        Task<T?> GetByIdAsync(int id);
        Task AddAsync(T entity);
        void Update(T entity);
        void Delete(T entity);
        
        // Operaciones de búsqueda
        Task<IEnumerable<T>> FindAsync(Expression<Func<T, bool>> predicate);
        Task<bool> ExistsAsync(Expression<Func<T, bool>> predicate);
    }
}