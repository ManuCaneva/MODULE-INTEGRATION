using System.Globalization;
using ApiDePapas.Application.Interfaces;
using System;
using System.Collections.Generic;
//Esto lo usamos para evitar la API real, mas adelante se puede cambiar
//si queremos usar una API real de geocodificación/rutas hay que cambiar esta clase o crear otra DistanceServiceExternal : IDistanceService que:
namespace ApiDePapas.Application.Services
{

    /// Estima distancia en km a partir de la PRIMERA letra del CPA argentino:
    /// usa centroides provinciales y fórmula de Haversine.
    /// Es un paso intermedio hasta integrar una API real de geocodificación/rutas.
    
    public class DistanceServiceInMemory : IDistanceService
    {
        public Task<double> GetDistanceKm(string originCpa, string destinationCpa)
        {
            char o = FirstLetter(originCpa);
            char d = FirstLetter(destinationCpa);

            if (!coords.TryGetValue(o, out var O) || !coords.TryGetValue(d, out var D))
                return Task.FromResult(300.0); // fallback neutro

            return Task.FromResult(HaversineKm(O.lat, O.lon, D.lat, D.lon));
        }

        private static char FirstLetter(string cpa)
            => string.IsNullOrWhiteSpace(cpa) ? 'H' : char.ToUpperInvariant(cpa.Trim()[0]);

        private static double HaversineKm(double lat1, double lon1, double lat2, double lon2)
        {
            const double R = 6371.0;
            double dLat = ToRad(lat2 - lat1);
            double dLon = ToRad(lon2 - lon1);
            double a = Math.Sin(dLat / 2) * Math.Sin(dLat / 2) +
                       Math.Cos(ToRad(lat1)) * Math.Cos(ToRad(lat2)) *
                       Math.Sin(dLon / 2) * Math.Sin(dLon / 2);
            double c = 2 * Math.Atan2(Math.Sqrt(a), Math.Sqrt(1 - a));
            return R * c;
        }

        private static double ToRad(double deg) => deg * Math.PI / 180.0;

        // Coordenadas aproximadas (lat, lon) por letra del CPA AR (capitales provinciales / centroides)
        private static readonly Dictionary<char, (double lat, double lon)> coords = new()
        {
            ['A']=(-24.79,-65.41), ['B']=(-34.61,-58.38), ['C']=(-34.60,-58.38), ['D']=(-33.30,-66.34),
            ['E']=(-31.73,-60.53), ['F']=(-29.41,-66.86), ['G']=(-27.79,-64.26), ['H']=(-27.45,-58.99),
            ['J']=(-31.54,-68.52), ['K']=(-28.47,-65.79), ['L']=(-36.62,-64.29), ['M']=(-32.89,-68.83),
            ['N']=(-27.36,-55.90), ['P']=(-26.18,-58.18), ['Q']=(-38.95,-68.06), ['R']=(-41.13,-71.31),
            ['S']=(-31.63,-60.70), ['T']=(-26.83,-65.22), ['U']=(-43.30,-65.10), ['V']=(-54.80,-68.30),
            ['W']=(-27.47,-58.83), ['X']=(-31.42,-64.18), ['Y']=(-24.19,-65.30), ['Z']=(-51.62,-69.22),
        };
    }
}
