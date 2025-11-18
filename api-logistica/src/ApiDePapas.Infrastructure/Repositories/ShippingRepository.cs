using ApiDePapas.Domain.Entities;
using ApiDePapas.Domain.Repositories;
using ApiDePapas.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;
using System.Linq.Expressions;

namespace ApiDePapas.Infrastructure.Repositories
{
    public class ShippingRepository : IShippingRepository
    {
        private readonly ApplicationDbContext _context;

        public ShippingRepository(ApplicationDbContext context)
        {
            _context = context;
        }
        
        // Implementación de IGenericRepository<ShippingDetail>
        public IQueryable<ShippingDetail> GetAllQueryable()
        {
            return _context.Shippings
                .Include(s => s.DeliveryAddress)
                    .ThenInclude(da => da.Locality)
                .Include(s => s.products)
                .Include(s => s.Travel)
                    .ThenInclude(t => t.TransportMethod);
        }

        public async Task<IEnumerable<ShippingDetail>> GetAllAsync()
        {
            return await GetAllQueryable().ToListAsync();
        }

        public async Task<ShippingDetail?> GetByIdAsync(int id)
        {
            Console.WriteLine($"\n--- INICIANDO DIAGNÓSTICO AVANZADO PARA SHIPPING ID: {id} ---");

            // PASO 1: Verificar el Shipping
            var shipping = await _context.Shippings.AsNoTracking().FirstOrDefaultAsync(s => s.shipping_id == id);
            if (shipping is null)
            {
                Console.WriteLine($"ERROR PASO 1: No se encontró el Shipping con id={id}.");
                return null;
            }
            Console.WriteLine($"OK PASO 1: Shipping {id} encontrado.");

            // PASO 2: Verificar el Travel y SUS dependencias
            var travel = await _context.Travels.AsNoTracking().FirstOrDefaultAsync(t => t.travel_id == shipping.travel_id);
            if (travel is null)
            {
                Console.WriteLine($"ERROR PASO 2: ¡CADENA ROTA! El 'Travel' con id={shipping.travel_id} NO EXISTE.");
                return null;
            }
            Console.WriteLine($"OK PASO 2: Travel {shipping.travel_id} encontrado. Verificando sus dependencias...");

            var transportMethod = await _context.TransportMethods.FindAsync(travel.transport_method_id);
            if (transportMethod is null) {
                Console.WriteLine($"ERROR PASO 2.1: ¡CADENA ROTA! El 'TransportMethod' con id={travel.transport_method_id} NO EXISTE.");
                return null;
            }
            
            var distributionCenter = await _context.DistributionCenters.FindAsync(travel.distribution_center_id);
            if (distributionCenter is null)
            {
                Console.WriteLine($"ERROR PASO 2.2: ¡CADENA ROTA! El 'DistributionCenter' con id={travel.distribution_center_id} NO EXISTE.");
                return null;
            }
            Console.WriteLine("OK PASO 2.x: Todas las dependencias de Travel existen.");

            // PASO 3: Verificar la Address y SUS dependencias
            var address = await _context.Addresses.AsNoTracking().FirstOrDefaultAsync(a => a.address_id == shipping.delivery_address_id);
            if (address is null)
            {
                Console.WriteLine($"ERROR PASO 3: ¡CADENA ROTA! La 'Address' con id={shipping.delivery_address_id} NO EXISTE.");
                return null;
            }
            Console.WriteLine($"OK PASO 3: Address {shipping.delivery_address_id} encontrada. Verificando sus dependencias...");

            var locality = await _context.Localities.FirstOrDefaultAsync(l => l.postal_code == address.postal_code && l.locality_name == address.locality_name);
            if (locality is null)
            {
                Console.WriteLine($"ERROR PASO 3.1: ¡CADENA ROTA! La 'Locality' con PK '{address.postal_code}/{address.locality_name}' NO EXISTE.");
                return null;
            }
            Console.WriteLine("OK PASO 3.1: La dependencia de Locality existe.");

            // Si llegamos hasta aquí, el problema es extremadamente raro o ya está resuelto.
            Console.WriteLine("\n--- TODAS LAS VERIFICACIONES PASARON. Ejecutando la consulta completa original... ---\n");
            
            // Devolvemos la consulta original
            return await _context.Shippings
                .Include(s => s.Travel).ThenInclude(t => t.TransportMethod)
                .Include(s => s.Travel).ThenInclude(t => t.DistributionCenter).ThenInclude(dc => dc.Address)
                .Include(s => s.DeliveryAddress).ThenInclude(a => a.Locality)
                .Include(s => s.products)
                .Include(s => s.logs)
                .AsSplitQuery()
                .FirstOrDefaultAsync(s => s.shipping_id == id);
        }

        public async Task AddAsync(ShippingDetail entity)
        {
            await _context.Shippings.AddAsync(entity);
            await _context.SaveChangesAsync();
        }

        public void Update(ShippingDetail entity)
        {
            _context.Shippings.Update(entity);
            _context.SaveChanges(); // Nota: En una app real, podrías usar un UnitOfWork
        }

        public void Delete(ShippingDetail entity)
        {
            _context.Shippings.Remove(entity);
            _context.SaveChanges();
        }

        public async Task<IEnumerable<ShippingDetail>> FindAsync(Expression<Func<ShippingDetail, bool>> predicate)
        {
            return await _context.Shippings.Where(predicate).ToListAsync();
        }

        public async Task<bool> ExistsAsync(Expression<Func<ShippingDetail, bool>> predicate)
        {
            return await _context.Shippings.AnyAsync(predicate);
        }

        // Implementaciones específicas de IShippingRepository
        public async Task<ShippingDetail?> GetByOrderIdAsync(int orderId)
        {
            return await GetByIdAsync(orderId); // Si el shipping_id es igual al order_id, sino ajustamos
        }
        
        public async Task<IEnumerable<ShippingDetail>> GetByUserIdAsync(int userId)
        {
            return await _context.Shippings
                .Where(s => s.user_id == userId)
                .ToListAsync();
        }

        public async Task UpdateStatusAsync(int shippingId, ShippingStatus newStatus)
        {
            var shipping = await _context.Shippings.FindAsync(shippingId);
            if (shipping != null)
            {
                shipping.status = newStatus;
                _context.Shippings.Update(shipping);
                await _context.SaveChangesAsync();
            }
        }
    }
}