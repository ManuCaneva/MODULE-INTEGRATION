/*using ApiDePapas.Application.DTOs;
using ApiDePapas.Domain;

namespace ApiDePapas.Application.Interfaces
{
    public interface IShippingStore
    {
        int Save(CreateShippingResponse response);
        CreateShippingResponse? Get(int id);
    }
}
*/
using ApiDePapas.Application.DTOs;

namespace ApiDePapas.Application.Interfaces
{
    public interface IShippingStore
    {
        int Save(CreateShippingResponse response);
        CreateShippingResponse? GetById(int shippingId);
        // Otros métodos necesarios para manejar envíos
        // Por ejemplo, actualizar estado, listar envíos, etc.
        //esto permite leer el envío por su ID

        CancelShippingResponse Cancel(int shippingId, DateTime now); 
        //esto permite cancelar un envío
        //cancel asumimos que el controller verifica que el envío existe y es valido para cancelar
    }
}