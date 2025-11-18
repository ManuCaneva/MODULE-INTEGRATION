using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using Microsoft.Extensions.Configuration;
using System.IO;

namespace ApiDePapas.Infrastructure.Persistence
{
    // 1. Cambiamos el tipo genérico a ApplicationDbContext
    public class DatabaseContextFactory : IDesignTimeDbContextFactory<ApplicationDbContext>
    {
        public ApplicationDbContext CreateDbContext(string[] args)
        {
            // Para asegurar que la fábrica busque appsettings.json en el directorio raíz de la API
            // El proyecto de Infraestructura no siempre es el directorio actual
            var environmentName = Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Development";
            
            var configuration = new ConfigurationBuilder()
                // Mueve la base de la ruta al directorio principal del proyecto (API)
                .SetBasePath(Path.Combine(Directory.GetCurrentDirectory(), "..", "ApiDePapas")) 
                .AddJsonFile("appsettings.json", optional: false)
                .AddJsonFile($"appsettings.{environmentName}.json", optional: true)
                .AddEnvironmentVariables()
                .Build();

            // Obtener la cadena de conexión
            var connectionString = configuration.GetConnectionString("DefaultConnection");

            // Opcional: DEBUG para confirmar que EF toma la cadena correcta
            Console.WriteLine($"[DEBUG] ConnectionString usada: {connectionString}");

            // Configurar el DbContext
            // 2. Cambiamos el tipo genérico a ApplicationDbContext
            var optionsBuilder = new DbContextOptionsBuilder<ApplicationDbContext>();
            
            // Usar MySql con la versión de servidor auto-detectada
            optionsBuilder.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString));

            // 3. Cambiamos el tipo devuelto a ApplicationDbContext
            return new ApplicationDbContext(optionsBuilder.Options);
        }
    }
}