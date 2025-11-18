# =========================================================
# ETAPA 1: BUILD (Construcción)
# =========================================================
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copia y restaura dependencias
COPY ["ApiDePapas.sln", "./"]
COPY src/ApiDePapas/ApiDePapas.csproj src/ApiDePapas/
COPY src/ApiDePapas.Domain/ApiDePapas.Domain.csproj src/ApiDePapas.Domain/
COPY src/ApiDePapas.Application/ApiDePapas.Application.csproj src/ApiDePapas.Application/
COPY src/ApiDePapas.Infrastructure/ApiDePapas.Infrastructure.csproj src/ApiDePapas.Infrastructure/
RUN dotnet restore "ApiDePapas.sln"

# Copia el resto del código y publica
COPY . .
WORKDIR "/src/src/ApiDePapas"
RUN dotnet publish "ApiDePapas.csproj" -c Release -o /app/publish

# =========================================================
# ETAPA 2: FINAL (Ejecución)
# ¡Usamos la imagen ASPNET liviana!
# =========================================================
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
EXPOSE 8080

# --- ¡CAMBIO AQUÍ! ---
# Instalamos netcat (para esperar) Y sed (para limpiar CSVs)
RUN apt-get update && apt-get install -y netcat-openbsd sed && \
    rm -rf /var/lib/apt/lists/*

# Copia SÓLO la aplicación compilada
COPY --from=build /app/publish .

# --- ¡LIMPIEZA! ---
# Borramos los comentarios viejos sobre 'db-init' porque ya no se usa.

# Copia el script de inicio (el NUEVO, simple)
COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]