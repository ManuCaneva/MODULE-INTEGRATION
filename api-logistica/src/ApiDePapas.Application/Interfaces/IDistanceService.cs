namespace ApiDePapas.Application.Interfaces
{
    public interface IDistanceService
    {
        /// <summary>
        /// Devuelve la distancia (km) entre dos CPA (códigos postales argentinos).
        /// Debe aceptar CPAs completos (ej: "H3500ABC") o al menos su primera letra.
        /// </summary>
        public Task<double> GetDistanceKm(string originCpa, string destinationCpa);
    }
}
