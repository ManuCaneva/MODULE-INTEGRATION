# DesarrolloAPP

## 🚀 Inicio Rápido

**¿Primera vez instalando?** → Lee **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** (5 minutos)

**¿Necesitas instrucciones detalladas?** → Lee **[INSTALACION.md](INSTALACION.md)** (completo)

**Ver responsabilidades** → Lee **[Responsabilidades](./documentacion/Responsabilidades/)** (completo)

### Instalación Express:

```bash
git clone https://github.com/Maximo-Vazquez/DesarrolloAPP.git
cd DesarrolloAPP
python -m venv venv
.\venv\Scripts\Activate.ps1    # Windows
pip install -r requirements.txt
python manage.py migrate
python verificar_instalacion.py  # ← Verifica que todo funciona ✅
```

---

## Principales Funcionalidades

- **Autenticación**:  
  - Login/registro tradicional y social (Google) usando [django-allauth](https://django-allauth.readthedocs.io/).
  - Modelo de usuario personalizado: [`administracion.Usuario`](apps/administracion/models.py).
  - Adaptador social para vincular cuentas por email: [`apps.login.adapters.MySocialAccountAdapter`](apps/login/adapters.py).

- **Administración**:  
  - Panel de administración personalizado.
  - Gestión de usuarios, productos y pedidos.

- **Pedidos y Clientes**:  
  - Gestión de pedidos, seguimiento y notificaciones por email.
  - Plantillas de emails para confirmación y entrega de pedidos en [`templates/emails/`](templates/emails/).

- **Frontend**:  
  - Plantillas base y componentes reutilizables.
  - Archivos estáticos organizados en carpetas por funcionalidad.

- **Docker**:  
  - Soporte para despliegue en Docker y scripts para construir y subir imágenes a Docker Hub en [`utils/imagenes/contruir_imagen.py`](utils/imagenes/contruir_imagen.py).

## Instalación y Ejecución

⚠️ **IMPORTANTE:** Lee primero [INSTALACION.md](INSTALACION.md) para instrucciones detalladas paso a paso.

### Instalación Rápida:

1. **Clonar el repositorio**  
   ```sh
   git clone https://github.com/Maximo-Vazquez/DesarrolloAPP.git
   cd DesarrolloAPP
   ```

2. **Crear y activar el entorno virtual**  
   
   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   
   **Linux/Mac:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**  
   ```sh
   pip install -r requirements.txt
   ```

4. **Ejecutar migraciones**  
   ```sh
   python manage.py migrate
   ```

5. **Verificar instalación**
   ```sh
   python verificar_instalacion.py
   ```

6. **Ejecutar servidor**
   ```sh
   python manage.py runserver
   ```
   
   O en Windows usar el script:
   ```cmd
   run.bat
   ```

### Acceder a la aplicación:

- **Aplicación web:** http://127.0.0.1:8000/
- **Swagger UI (APIs):** http://127.0.0.1:8000/api/docs/
- **Admin Panel:** http://127.0.0.1:8000/admin/

### Ejecutar pruebas:

```sh
# Script de pruebas completo
python tests/test_apis_mock_completo.py

# Pruebas unitarias
python manage.py test
```
7. **Iniciar el servidor de desarrollo**  
   ```sh
   python manage.py runserver
   ```
8. **Acceder a la aplicación**  
   - Navegar a `http://127.0.0.1:8000/` en un navegador web.

## Notas

- Asegurarse de tener Docker y Docker Compose instalados si se va a utilizar la funcionalidad de Docker.
- Revisar la documentación de cada herramienta y librería utilizada para más detalles sobre su uso y configuración.

# Configuración
-Variables principales en Main/settings.py.
-Configuración de correo para notificaciones y recuperación de contraseña.
-Configuración de autenticación social en la sección SOCIALACCOUNT_PROVIDERS.

# Notas
- El modelo de usuario personalizado requiere que AUTH_USER_MODEL = 'administracion.Usuario' esté definido antes de la primera migración.
- Las rutas principales están definidas en Main/urls.py.
- El entorno incluye scripts para facilitar el desarrollo y despliegue (run.bat, makemigrations.bat, etc.).