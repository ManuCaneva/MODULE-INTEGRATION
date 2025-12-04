# login

Módulo de autenticación y gestión de sesiones. Integra autenticación tradicional (email/contraseña) con autenticación social (Google OAuth) mediante django-allauth.

---

## 📁 Responsabilidades de cada archivo

### **`views.py`**
Maneja las vistas de autenticación:
- **`login_view()`**: Procesa inicio de sesión con email y contraseña
- **`registro_view()`**: Registra nuevos usuarios validando duplicados de email/username
- **`cerrar_sesion()`**: Cierra la sesión del usuario

### **`backends.py`**
Backend de autenticación personalizado que permite login usando email en lugar de username.


### **`signals.py`**
Señal que genera automáticamente un username único basado en el email del usuario cuando no se proporciona uno.

### **`urls.py`**
Define las rutas del módulo:
- `/login/` - Formulario de inicio de sesión
- `/registro/` - Formulario de registro
- `/cerrar-sesion/` - Cierre de sesión

### **`templates/login_registro.html`**
Template con diseño moderno que presenta:
- Formulario de login con email/contraseña
- Link para registro de nuevos usuarios

### **`apps.py`**
Configuración de la aplicación Django que registra las señales al iniciar.

### **`models.py`**, **`admin.py`**, **`tests.py`**
Archivos de configuración estándar de Django (actualmente sin contenido específico).
