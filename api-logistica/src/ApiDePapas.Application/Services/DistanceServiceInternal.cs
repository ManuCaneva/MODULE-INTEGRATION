using System;
using System.Globalization;
using System.Collections.Generic;

using ApiDePapas.Application.Interfaces;
using ApiDePapas.Domain.Entities;
using ApiDePapas.Domain.Repositories;

// Es una mejor aproximación que DistanceServiceInMemory. Sirve para
// calcular distancias entre departamentos en lugar de provincias, por lo
// que usa los 5 primeros dígitos del código postal y promedia las coordenadas
// geográficas de las localidades con ese código postal.

// Puede utilizarse una API externa en el futuro si se quiere precisión a nivel
// calle/dirección.

namespace ApiDePapas.Application.Services
{
    public class DistanceServiceInternal : IDistanceService
    {
        private readonly ILocalityRepository _locality_repository;

        public DistanceServiceInternal(
            ILocalityRepository localityRepository)
        {
            _locality_repository = localityRepository;
        }

        public (double lat, double lon) GetAverageCoordinates(List<(double, double)> points)
        {
            if (points == null || !points.Any())
            {
                throw new ArgumentException("La lista de puntos no puede ser nula o vacía.");
            }

            double x = 0.0;
            double y = 0.0;
            double z = 0.0;

            int count = 0;

            foreach (var (latDeg, lonDeg) in points)
            {
                double latRad = DegreesToRadians(latDeg);
                double lonRad = DegreesToRadians(lonDeg);

                double cosLat = Math.Cos(latRad);

                x += cosLat * Math.Cos(lonRad);
                y += cosLat * Math.Sin(lonRad);
                z += Math.Sin(latRad);

                count++;
            }

            x /= count;
            y /= count;
            z /= count;

            double lonCenter = Math.Atan2(y, x);
            double hyp = Math.Sqrt(x * x + y * y);
            double latCenter = Math.Atan2(z, hyp);

            return (RadiansToDegrees(latCenter), RadiansToDegrees(lonCenter));
        }

        public async Task<double> GetDistanceKm(string originCpa, string destinationCpa)
        {
            List<Locality> possibleOriginLocalities = _locality_repository.GetByPostalCodeAsync(originCpa).Result;
            List<Locality> possibleDestinationLocalities = _locality_repository.GetByPostalCodeAsync(destinationCpa).Result;

            if (!possibleOriginLocalities.Any() || !possibleDestinationLocalities.Any()) { return 300.0; } // fallback neutro

            List<(double lat, double lon)> possibleOriginCoords = possibleOriginLocalities
                .Select(l => ((double)l.lat, (double)l.lon))
                .ToList();

            List<(double lat, double lon)> possibleDestinationCoords = possibleDestinationLocalities
                .Select(l => ((double)l.lat, (double)l.lon))
                .ToList();

            (double lat, double lon) originCentroid = GetAverageCoordinates(possibleOriginCoords);
            (double lat, double lon) destinationCentroid = GetAverageCoordinates(possibleDestinationCoords);

            return HaversineKm(originCentroid.lat, originCentroid.lon, destinationCentroid.lat, destinationCentroid.lon);
        }

        private static double HaversineKm(double lat1, double lon1, double lat2, double lon2)
        {
            const double R = 6371.0;
            double dLat = DegreesToRadians(lat2 - lat1);
            double dLon = DegreesToRadians(lon2 - lon1);
            double a = Math.Sin(dLat / 2) * Math.Sin(dLat / 2) +
                       Math.Cos(DegreesToRadians(lat1)) * Math.Cos(DegreesToRadians(lat2)) *
                       Math.Sin(dLon / 2) * Math.Sin(dLon / 2);
            double c = 2 * Math.Atan2(Math.Sqrt(a), Math.Sqrt(1 - a));
            return R * c;
        }

        private static double DegreesToRadians(double degrees) => degrees * (double)Math.PI / 180.0f;
        private static double RadiansToDegrees(double radians) => radians * 180.0f / (double)Math.PI;
    }
}
