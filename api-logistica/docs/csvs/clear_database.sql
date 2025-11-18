USE apidepapas;

-- 1. DESACTIVAR LA VERIFICACIÓN DE CLAVES FORÁNEAS (LA FORMA RÁPIDA DE LIMPIAR)
SET FOREIGN_KEY_CHECKS = 0;

-- 2. TRUNCAR TABLAS EN ORDEN SEGURO (DEL DEPENDIENTE AL PADRE)
-- El orden inverso de las dependencias:

-- Tablas que dependen de Shippings (Hijos directos)
TRUNCATE TABLE ProductQty;
TRUNCATE TABLE ShippingLog;

-- Tablas dependientes (Intermedias/Principales)
TRUNCATE TABLE Shippings;
TRUNCATE TABLE Travels;
TRUNCATE TABLE DistributionCenters;

-- Tablas de Catálogo (Padres)
TRUNCATE TABLE TransportMethods;

-- Tablas Base (Padres)
TRUNCATE TABLE Addresses;
TRUNCATE TABLE Localities;

-- Opcional: Limpiar el historial de migraciones si planeas recrear el esquema
TRUNCATE TABLE __EFMigrationsHistory; 

-- 3. REACTIVAR LA VERIFICACIÓN DE CLAVES FORÁNEAS
SET FOREIGN_KEY_CHECKS = 1;