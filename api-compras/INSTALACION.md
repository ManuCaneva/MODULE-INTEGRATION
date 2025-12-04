# 🚀 Guía de Instalación - DesarrolloAPP

Esta guía te ayudará a configurar el proyecto en tu máquina local.

---

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.12 o 3.13** → [Descargar Python](https://www.python.org/downloads/)
- **Git** → [Descargar Git](https://git-scm.com/downloads)
- **Visual Studio Code** (recomendado) → [Descargar VS Code](https://code.visualstudio.com/)

---

## 🔧 Instalación Paso a Paso

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/Maximo-Vazquez/DesarrolloAPP.git
cd DesarrolloAPP
```

### 2️⃣ Crear Entorno Virtual

**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> ⚠️ **Importante:** Si tienes error de permisos en PowerShell, ejecuta:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 3️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- ✅ Django 5.2.6
- ✅ Django REST Framework 3.16.1
- ✅ drf-spectacular 0.28.0 (Swagger/OpenAPI)
- ✅ django-allauth (Autenticación)
- ✅ requests (Cliente HTTP)
- ✅ Y todas las demás dependencias

### 4️⃣ Aplicar Migraciones

```bash
python manage.py migrate
```

### 5️⃣ Crear Datos de Prueba

**⚠️ IMPORTANTE:** Sin este paso, las APIs Mock estarán vacías y no funcionarán.

```bash
python crear_datos_prueba.py
```

Este script crea automáticamente:
- ✅ 4 Categorías de productos
- ✅ 15 Productos con stock
- ✅ 4 Métodos de transporte

### 6️⃣ Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

### 7️⃣ Ejecutar el Servidor

**Opción A - Comando manual:**
```bash
python manage.py runserver
```

**Opción B - Usando el script BAT (solo Windows):**
```cmd
run.bat
```

El servidor estará disponible en: **http://127.0.0.1:8000/**

### 8️⃣ Verificar que todo funciona correctamente ✅

**¡IMPORTANTE!** Ejecuta este comando para verificar que todo está bien instalado:

```bash
python verificar_instalacion.py
```

Si ves el mensaje **"🎉 ¡TODO ESTÁ CORRECTAMENTE INSTALADO! 🎉"**, ¡estás listo para trabajar!

Si hay errores, el script te dirá exactamente qué falta y cómo solucionarlo.

---

## 📚 Documentación de APIs

Una vez que el servidor esté corriendo, puedes acceder a:

- **Swagger UI (Interactivo):** http://127.0.0.1:8000/api/docs/
- **ReDoc (Documentación):** http://127.0.0.1:8000/api/redoc/
- **Schema JSON:** http://127.0.0.1:8000/api/schema/

---

## 🧪 Ejecutar Pruebas

### Ejecutar TODAS las pruebas:
```bash
python manage.py test
```

### Ejecutar script de pruebas Mock APIs:
```bash
python tests/test_apis_mock_completo.py
```

### Ejecutar pruebas específicas:
```bash
# Pruebas de Stock API
python manage.py test tests.test_stock_api -v 2

# Pruebas de Logística API
python manage.py test tests.test_logistica_api -v 2

# Pruebas E2E (End-to-End)
python manage.py test tests.test_integration_e2e -v 2
```

---

## 🛠️ Extensiones Recomendadas para VS Code

Abre VS Code y busca estas extensiones:

1. **Python** (ms-python.python) - Soporte completo para Python
2. **Pylance** (ms-python.vscode-pylance) - IntelliSense mejorado
3. **Django** (batisteo.vscode-django) - Snippets y sintaxis Django
4. **REST Client** (humao.rest-client) - Probar APIs desde VS Code
5. **SQLite Viewer** (alexcvzz.vscode-sqlite) - Ver base de datos

### Instalación rápida desde terminal:

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension batisteo.vscode-django
code --install-extension humao.rest-client
code --install-extension alexcvzz.vscode-sqlite
```

---

## 📂 Estructura del Proyecto

```
DesarrolloAPP/
│
├── Main/                          # Configuración principal de Django
│   ├── settings.py               # Configuración del proyecto
│   ├── urls.py                   # URLs principales
│   └── wsgi.py
│
├── apps/                          # Aplicaciones Django
│   ├── administracion/           # App de administración
│   ├── apis/                     # APIs Mock y endpoints
│   │   ├── stockApi/            # API Mock de Stock
│   │   └── logisticaApi/        # API Mock de Logística
│   ├── inicio/                   # App de inicio
│   ├── login/                    # App de autenticación
│   └── modulos/                  # Módulos del sistema
│
├── tests/                         # Pruebas automatizadas
│   ├── test_apis_mock_completo.py    # Script de pruebas E2E
│   ├── test_stock_api.py             # Tests unitarios Stock
│   ├── test_logistica_api.py         # Tests unitarios Logística
│   └── test_integration_e2e.py       # Tests de integración
│
├── static/                        # Archivos estáticos (CSS, JS, imágenes)
├── templates/                     # Plantillas HTML
├── documentacion/                 # Documentación del proyecto
│
├── requirements.txt               # 📦 Dependencias Python
├── manage.py                      # CLI de Django
├── db.sqlite3                     # Base de datos SQLite
└── README.md                      # Documentación principal
```

---

## 🔍 Verificar Instalación

### Método Rápido (Recomendado) ⚡

Ejecuta el script de verificación automática:

```bash
python verificar_instalacion.py
```

Este script verifica automáticamente:
- ✅ Versión de Python
- ✅ Todos los paquetes instalados
- ✅ Configuración de Django
- ✅ Migraciones aplicadas
- ✅ Que el servidor puede iniciar

**Salida esperada:**
```
🎉 ¡TODO ESTÁ CORRECTAMENTE INSTALADO! 🎉

Próximos pasos:
   1. Ejecuta: python manage.py runserver
   2. Visita: http://127.0.0.1:8000/api/docs/
   3. Ejecuta las pruebas: python tests/test_apis_mock_completo.py
```

### Verificación Manual (Opcional)

Si prefieres verificar manualmente cada cosa:

```bash
# 1. Verificar que el entorno virtual está activo
#    Deberías ver (venv) al inicio de tu terminal

# 2. Verificar versión de Python
python --version

# 3. Verificar paquetes instalados
pip list

# 4. Verificar Django
python manage.py --version

# 5. Verificar que el servidor inicia
python manage.py check

# 6. Ejecutar pruebas
python tests/test_apis_mock_completo.py
```

Si ves **"🎉 ¡TODAS LAS PRUEBAS PASARON! 🎉"**, ¡todo está bien configurado! ✅

---

## ❓ Problemas Comunes

### Error: `ModuleNotFoundError: No module named 'rest_framework'`
**Solución:** Asegúrate de que el entorno virtual esté activo y ejecuta:
```bash
pip install -r requirements.txt
```

### Error: `(venv) no se reconoce como comando`
**Solución:** Activa el entorno virtual primero:
```powershell
.\venv\Scripts\Activate.ps1
```

### Error: `django.db.utils.OperationalError: no such table`
**Solución:** Ejecuta las migraciones:
```bash
python manage.py migrate
```

### El servidor no inicia
**Solución:** Verifica que el puerto 8000 no esté en uso:
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

---

## 📞 Contacto y Ayuda

Si tienes problemas con la instalación:

1. Revisa la documentación en `/documentacion/`
2. Consulta `GUIA_RAPIDA_USO.md`
3. Contacta al equipo de desarrollo

---

## 🎯 Próximos Pasos

Una vez instalado:

1. ✅ Familiarízate con la estructura del proyecto
2. ✅ Revisa la documentación de las APIs en Swagger
3. ✅ Ejecuta las pruebas para entender el flujo
4. ✅ Lee `documentacion/IMPLEMENTACION_COMPLETADA.md`

---

**¡Listo para empezar a desarrollar! 🚀**
