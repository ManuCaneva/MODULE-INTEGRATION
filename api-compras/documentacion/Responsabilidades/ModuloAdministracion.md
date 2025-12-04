# administracion

Módulo de administración y gestión de usuarios del sistema. Proporciona un panel de control (dashboard) para visualizar métricas, transacciones y gestionar configuraciones.

---

## 📁 Estructura de archivos

### **`models.py`**
Define el modelo de usuario personalizado del sistema:

#### **`Usuario`** (heredado de `AbstractUser`)
Modelo de usuario extendido con campos adicionales:

**Campos heredados de AbstractUser**:
- `username`: Nombre de usuario único
- `email`: Correo electrónico
- `password`: Contraseña hasheada
- `first_name`: Nombre
- `last_name`: Apellido
- `is_active`: Usuario activo
- `is_staff`: Acceso al Django Admin
- `is_superuser`: Permisos de superusuario
- `date_joined`: Fecha de registro en el sistema

**Campos personalizados**:
- `telefono`: Número de teléfono (max 20 caracteres, opcional)
- `direccion`: Dirección de texto libre (opcional)
- `vac`: Booleano para verificación adicional de cuenta (default: False)
- `fecha_nacimiento`: Fecha de nacimiento (opcional)
- `fecha_registro`: Timestamp automático de registro (auto_now_add)

**Configuración del modelo**:
- `db_table`: "usuario" (nombre de tabla en base de datos)
- `verbose_name`: "Usuario" / "Usuarios" (configuración Django Admin)
- `__str__()`: Representación detallada con todos los campos

**Relaciones con otros modelos**:
- `Pedido.usuario`: ForeignKey desde pedidoApi (nullable para pedidos anónimos)
- `Carrito.usuario`: ForeignKey desde carritoApi (nullable)
- `DireccionEnvio.usuario`: ForeignKey desde pedidoApi (nullable)

**Responsabilidad**: Modelo central de autenticación y autorización. Extiende el usuario estándar de Django con información adicional de perfil. Usado por django-allauth para autenticación social y tradicional.

---

### **`views.py`**
Vistas del panel de administración:

#### **`_dashboard_context()`** (función auxiliar privada)
Genera datos mock para el dashboard:
- **KPIs**:
  - `kpi_ingresos`: "1.250.000" (ingresos totales simulados)
  - `kpi_usuarios_nuevos`: 42 (usuarios registrados recientemente)
  - `kpi_items`: 318 (productos o ítems totales)
  - `kpi_ordenes_ok`: 289 (pedidos completados exitosamente)
- **Transacciones**:
  - Lista de 3 transacciones de ejemplo con ID, usuario, monto, fecha y estado

**Nota**: Esta función contiene datos hardcodeados. Reemplazar con consultas reales a modelos de Pedido, Usuario, etc.

---

#### **`administracion_view(request)`**
Vista principal del panel de administración:
- **Ruta**: `/administracion/`
- **Template**: `inicio_admin.html`
- **Contexto**: Datos del dashboard desde `_dashboard_context()`
- **Autenticación**: Actualmente sin restricciones (comentado `@login_required`)

**Responsabilidad**: Renderiza el dashboard principal con métricas y transacciones recientes.

---

#### **Vistas placeholder**
Rutas temporales para evitar errores de navegación:

##### **`admin_items_nuevo(request)`**
- **Propósito**: Placeholder para "Nuevo ítem"
- **Estado**: Redirige temporalmente al dashboard
- **Futuro**: Reemplazar con formulario para crear productos/categorías

##### **`admin_reportes(request)`**
- **Propósito**: Placeholder para "Reportes"
- **Estado**: Redirige temporalmente al dashboard
- **Futuro**: Implementar generación de reportes (ventas, usuarios, stock)

##### **`admin_config(request)`**
- **Propósito**: Placeholder para "Configuración"
- **Estado**: Redirige temporalmente al dashboard
- **Futuro**: Configuración del sistema (métodos de pago, envío, notificaciones)

##### **`admin_transacciones(request)`**
- **Propósito**: Placeholder para "Transacciones"
- **Estado**: Redirige temporalmente al dashboard
- **Futuro**: Listado completo de transacciones con filtros y búsqueda

**Responsabilidad**: Proporcionar estructura de navegación sin errores 404 mientras se desarrollan las funcionalidades completas.

---

### **`urls.py`**
Configuración de rutas del módulo:

**Rutas definidas**:
```python
path('', views.administracion_view, name='administracion')
path('items/nuevo/', views.administracion_view, name='admin_items_nuevo')
path('reportes/', views.administracion_view, name='admin_reportes')
path('configuracion/', views.administracion_view, name='admin_config')
path('transacciones/', views.administracion_view, name='admin_transacciones')
```

**Nota**: Todas las rutas secundarias apuntan temporalmente a `administracion_view` para evitar errores. Reemplazar con vistas específicas cuando estén implementadas.

**Responsabilidad**: Enrutamiento del panel de administración. Todas las URLs bajo `/administracion/*`.

---

### **`templates/inicio_admin.html`**
Template del dashboard de administración:

**Extiende**: `baseAdmin.html` (layout base del panel administrativo)

**Estructura HTML**:
- **Tabla de últimas transacciones**:
  - Columnas: ID, Usuario, Monto, Fecha, Estado
  - Estados visuales: OK (verde), Pendiente (amarillo), Error (rojo)
  - Botón "Ver todas" → redirige a `admin_transacciones`
  - Mensaje de tabla vacía si no hay datos

**Contexto esperado**:
- `ultimas_transacciones`: Lista de diccionarios con:
  - `id`: ID de la transacción
  - `usuario`: Nombre de usuario
  - `monto`: Monto formateado (string)
  - `fecha`: Datetime (formateado como "dd/mm/YYYY HH:mm")
  - `estado`: "OK" / "PENDIENTE" / "ERROR"

**Estilos aplicados**:
- Clases CSS: `card`, `table`, `chip` (definidas en `baseAdmin.html` o archivos CSS)
- Iconos: Boxicons (`bx-right-arrow-alt`)

**Responsabilidad**: Presentación visual del dashboard administrativo con tabla de transacciones recientes.

---

### **`apps.py`**
Configuración de la aplicación Django:

```python
class AdministracionConfig(AppConfig):
    name = 'apps.modulos.administracion'
    default_auto_field = 'django.db.models.BigAutoField'
```

**Responsabilidad**: Metadatos y configuración de la app para el registro en `INSTALLED_APPS`.

---

### **`admin.py`**
Registro de modelos en Django Admin (actualmente vacío).

**Responsabilidad**: Configurar el panel de Django Admin (`/admin/`) para gestionar usuarios, permisos y grupos. 

**Pendiente**: Registrar modelo `Usuario` con configuración personalizada:
```python
from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'telefono', 'is_active', 'is_staff', 'fecha_registro']
    list_filter = ['is_active', 'is_staff', 'vac', 'fecha_registro']
    search_fields = ['username', 'email', 'telefono']
    readonly_fields = ['fecha_registro', 'date_joined']
```

---

### **`tests.py`**
Archivo para pruebas unitarias (actualmente con imports básicos).

**Responsabilidad**: Testing del módulo de administración. Debe contener pruebas para:
- Creación de usuarios con campos personalizados
- Autenticación y autorización
- Acceso al dashboard (con/sin login)
- Validación de campos del modelo Usuario
- Representación string del usuario

---

## 🔗 Dependencias

### **Django Auth System**
- `AbstractUser`: Modelo base para Usuario
- `Group`, `Permission`: Gestión de permisos y roles
- django-allauth: Autenticación social y registro

### **Otros módulos internos**
- **pedidoApi**: Relación `Pedido.usuario`
- **carritoApi**: Relación `Carrito.usuario`

---

## 🔧 Configuración requerida

En `settings.py`:

```python
# Modelo de usuario personalizado
AUTH_USER_MODEL = 'administracion.Usuario'

# django-allauth
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'apps.modulos.administracion',
    # ...
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configuración de allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

En `Main/urls.py`:

```python
urlpatterns = [
    path('administracion/', include('apps.modulos.administracion.urls')),
    path('accounts/', include('allauth.urls')),
    # ...
]
```

---

## 📊 Flujo de datos

### **Acceso al dashboard**:
```
Usuario → /administracion/ → administracion_view()
    ↓
_dashboard_context() genera datos mock
    ↓
Renderiza inicio_admin.html con KPIs y transacciones
```

### **Navegación interna**:
```
Usuario → Click en "Reportes"
    ↓
/administracion/reportes/ → administracion_view() (placeholder)
    ↓
Renderiza mismo dashboard (temporal)
```

---

## 🧪 Testing

Para ejecutar las pruebas del módulo:

```powershell
python manage.py test apps.modulos.administracion
```

---

## 📝 Notas de implementación

1. **Modelo de usuario personalizado**: Se define `AUTH_USER_MODEL = 'administracion.Usuario'` en settings. Esto debe hacerse **antes de la primera migración**.

2. **Datos mock en vistas**: La función `_dashboard_context()` contiene datos hardcodeados. Reemplazar con:
   ```python
   from apps.apis.pedidoApi.models import Pedido
   from .models import Usuario
   
   def _dashboard_context():
       total_usuarios = Usuario.objects.filter(is_active=True).count()
       pedidos_ok = Pedido.objects.filter(estado='confirmado').count()
       ingresos = Pedido.objects.filter(estado='confirmado').aggregate(total=Sum('total'))['total']
       # ...
   ```

3. **Vistas placeholder**: Todas las rutas secundarias (`reportes/`, `configuracion/`, etc.) apuntan temporalmente a `administracion_view`. Reemplazar con vistas específicas cuando se implementen.

4. **Sin autenticación forzada**: El decorator `@login_required` está comentado. Descomentar para producción:
   ```python
   @login_required
   def administracion_view(request):
       # ...
   ```

5. **Campos opcionales del Usuario**: Los campos `telefono`, `direccion`, `fecha_nacimiento` son opcionales (`blank=True, null=True`). Validar en formularios si se requieren.

6. **Campo `vac`**: Probablemente sea "Verified Account" o similar. Documentar su propósito específico.

7. **Django Admin vacío**: El archivo `admin.py` está vacío. Registrar el modelo Usuario para gestión desde `/admin/`.

8. **Template extendido**: `inicio_admin.html` extiende `baseAdmin.html`. Asegurar que este template base incluya:
   - Navegación lateral con enlaces a reportes, configuración, etc.
   - KPIs en la parte superior (ingresos, usuarios, ítems, órdenes)
   - Estilos CSS para `.card`, `.table`, `.chip`

9. **Iconos Boxicons**: El template usa Boxicons (`bx-right-arrow-alt`). Asegurar que esté incluido en `baseAdmin.html`:
   ```html
   <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
   ```

10. **Migración del modelo Usuario**: Al cambiar `AUTH_USER_MODEL`, ejecutar:
    ```powershell
    python manage.py makemigrations
    python manage.py migrate
    ```
    Si ya existen datos, puede requerir migraciones personalizadas.

---

## 🚀 Próximos pasos (desarrollo futuro)

1. **Implementar reportes**: Gráficos de ventas, usuarios activos, productos más vendidos (usar Chart.js o similar)

2. **Configuración del sistema**: Formularios para ajustar:
   - Métodos de pago aceptados
   - Zonas de envío y costos
   - Notificaciones por email

3. **Gestión de transacciones**: Vista completa con filtros por fecha, usuario, estado

4. **Gestión de productos**: CRUD completo de productos/categorías (actualmente solo lectura desde Stock API)

5. **Permisos granulares**: Implementar roles (Admin, Staff, Vendedor) con permisos específicos usando Django `Group` y `Permission`

6. **Auditoría**: Log de acciones administrativas (crear/editar/eliminar productos, cambios de estado de pedidos)

7. **Dashboard interactivo**: Reemplazar datos mock con datos reales y gráficos dinámicos

8. **Exportación de datos**: Botones para exportar reportes en CSV/Excel/PDF
