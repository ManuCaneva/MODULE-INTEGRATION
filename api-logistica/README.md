# 2025-06-TPI
Desarrollo de Software 2025 - Grupo 06 - TPI

## 🚀 Proyecto ApiDePapas - Guía de Inicio Rápido
Este proyecto está completamente "dockerizado" para garantizar un entorno de desarrollo consistente para todo el equipo. Con un solo comando, tendrás la base de datos y la API funcionando.

---

### ✅ Prerrequisitos
Antes de empezar, asegurate de tener instalado y corriendo:
* Git
* Docker Desktop

---

### 📝 Puesta en Marcha (La Primera Vez)
Seguí estos pasos para levantar el proyecto desde cero.

1.  **Clonar el Repositorio**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    ```

2.  **Entrar a la Carpeta**
    ```bash
    cd <NOMBRE_DE_LA_CARPETA_DEL_PROYECTO>
    ```

3.  **Construir y Levantar los Contenedores**
    Este es el único comando que necesitás. Construirá la imagen de la API, creará los contenedores, aplicará las migraciones y cargará los datos de prueba.
    ```bash
    docker compose up --build
    ```

4.  **Verificar que Funciona**
    Esperá a que los logs en la terminal muestren el mensaje: `info: Microsoft.Hosting.Lifetime[14] Now listening on: http://[::]:8080`.
    
    Una vez que aparezca, abrí tu navegador y andá a la interfaz de Swagger para probar la API:
    **[http://localhost:5001/swagger](http://localhost:5001/swagger)**

---

### 👨‍💻 Cómo Usar la API (Ejemplo: Crear un Envío)
Para crear un envío (`Shipping`), necesitás usar los IDs de productos que ya existan en la base de datos.

#### 1. Buscar un ID de Producto Válido
Los datos de prueba ya incluyen productos. Para ver algunos, abrí **una nueva terminal** y conectate a la base de datos:

```bash
docker exec -it apipapas_mysql mysql -u ApiUser -p
```
* Te pedirá la contraseña: `ApiDePapas_G6_Logistica`

Una vez adentro (`mysql>`), ejecutá esta consulta para ver 5 productos:

```sql
USE apidepapas;
SELECT * FROM Products LIMIT 5;
```
Anotá uno de los `id` que te aparezcan.

#### 2. Enviar la Petición POST
Ahora, andá a Swagger o Postman y enviá una petición `POST` a la ruta `/shipping` usando el `id` que encontraste.

* **Método:** `POST`
* **URL:** `http://localhost:5001/shipping`
* **Body (JSON):**
    ```json
    {
      "order_id": 1234,
      "user_id": 567,
      "delivery_address": {
        "street": "Avenida Corrientes",
        "number": 900,
        "postal_code": "C1043",
        "locality_name": "Buenos Aires"
      },
      "transport_type": "truck",
      "products": [
        {
          "id": 105,
          "quantity": 2
        }
      ]
    }
    ```
Si todo sale bien, recibirás un `200 OK` con los datos del envío recién creado.

---

### 🔄 Ciclo de Vida (El Día a Día)

#### Para Parar Todo (y guardar los datos) 🛑
Cuando termines de trabajar, volvé a la terminal donde corrían los logs y presioná `Ctrl + C`. Luego, ejecutá:
```bash
docker compose down
```
Esto detiene y elimina los contenedores, pero **tus datos se mantienen seguros** en un volumen de Docker.

#### Para Volver a Arrancar 💾
La próxima vez que quieras trabajar, simplemente ejecutá:
```bash
docker compose up
```
Notarás que el script se salta las migraciones porque detecta que la base de datos ya está inicializada. Todos los `INSERT` que hiciste seguirán ahí.

#### Para Empezar de Cero (Borrón y Cuenta Nueva) 💥
Si querés eliminar **TODO**, incluyendo la base de datos, para empezar desde cero, usá el comando `down` con la opción `-v` (de volúmenes).
```bash
docker compose down -v
```
**¡Ojo! Esto borra todos los datos de la base de datos de forma permanente.**
