namespace ApiDePapas.Application.Interfaces
{
    /**
     * Define el contrato para un servicio que gestiona
     * la obtención de tokens de autenticación.
     */
    public interface ITokenService
    {
        Task<string> GetAccessTokenAsync();
    }
}