"""
Script de Verificación de Instalación
Ejecuta este script para verificar que todo está correctamente instalado
"""
import sys
import subprocess
import importlib

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def print_ok(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def check_python_version():
    print_header("Verificando versión de Python")
    version = sys.version_info
    print_info(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 12:
        print_ok("Versión de Python correcta (3.12+)")
        return True
    else:
        print_error("Se requiere Python 3.12 o superior")
        return False

def check_package(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'sin versión')
        print_ok(f"{package_name}: {version}")
        return True
    except ImportError:
        print_error(f"{package_name} NO está instalado")
        return False

def check_django_setup():
    print_header("Verificando configuración de Django")
    try:
        import django
        from django.conf import settings
        
        # Configurar Django
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')
        django.setup()
        
        print_ok("Django configurado correctamente")
        print_info(f"DEBUG = {settings.DEBUG}")
        print_info(f"Base de datos: {settings.DATABASES['default']['ENGINE']}")
        return True
    except Exception as e:
        print_error(f"Error al configurar Django: {str(e)}")
        return False

def check_migrations():
    print_header("Verificando migraciones")
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'showmigrations'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Contar migraciones aplicadas
            applied = result.stdout.count('[X]')
            unapplied = result.stdout.count('[ ]')
            
            print_info(f"Migraciones aplicadas: {applied}")
            
            if unapplied > 0:
                print_error(f"Migraciones pendientes: {unapplied}")
                print_info("Ejecuta: python manage.py migrate")
                return False
            else:
                print_ok("Todas las migraciones están aplicadas")
                return True
        else:
            print_error("Error al verificar migraciones")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def check_server():
    print_header("Verificando que el servidor puede iniciar")
    print_info("Esta prueba puede tardar unos segundos...")
    
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'check'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print_ok("El servidor puede iniciar sin problemas")
            return True
        else:
            print_error("Hay problemas con la configuración del servidor")
            print_info(result.stdout)
            print_info(result.stderr)
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def check_datos_prueba():
    print_header("Verificando datos de prueba")
    try:
        from apps.apis.stockApi.models import Producto, Categoria
        from apps.apis.logisticaApi.models import MetodoTransporte
        
        productos = Producto.objects.count()
        categorias = Categoria.objects.count()
        metodos = MetodoTransporte.objects.count()
        
        if productos > 0 and categorias > 0 and metodos > 0:
            print_ok(f"Datos de prueba encontrados:")
            print_info(f"  - Productos: {productos}")
            print_info(f"  - Categorías: {categorias}")
            print_info(f"  - Métodos de transporte: {metodos}")
            return True
        else:
            print_error("No hay datos de prueba en la base de datos")
            print_info("Ejecuta: python crear_datos_prueba.py")
            return False
    except Exception as e:
        print_error(f"Error al verificar datos: {str(e)}")
        print_info("Ejecuta: python crear_datos_prueba.py")
        return False

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║          VERIFICACIÓN DE INSTALACIÓN - DesarrolloAPP             ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    results = []
    
    # Verificar Python
    results.append(check_python_version())
    
    # Verificar paquetes instalados
    print_header("Verificando paquetes instalados")
    packages = [
        ('Django', 'django'),
        ('Django REST Framework', 'rest_framework'),
        ('drf-spectacular', 'drf_spectacular'),
        ('django-allauth', 'allauth'),
        ('requests', 'requests'),
        ('PyJWT', 'jwt'),
    ]
    
    for package_name, import_name in packages:
        results.append(check_package(package_name, import_name))
    
    # Verificar Django
    results.append(check_django_setup())
    
    # Verificar migraciones
    results.append(check_migrations())
    
    # Verificar datos de prueba
    results.append(check_datos_prueba())
    
    # Verificar servidor
    results.append(check_server())
    
    # Resumen final
    print_header("RESUMEN FINAL")
    total = len(results)
    exitosos = sum(results)
    fallidos = total - exitosos
    
    print_info(f"Total de verificaciones: {total}")
    print_ok(f"Exitosas: {exitosos}")
    
    if fallidos > 0:
        print_error(f"Fallidas: {fallidos}")
        print("\n⚠️  Por favor, revisa los errores anteriores y:")
        print("   1. Asegúrate de que el entorno virtual esté activado")
        print("   2. Ejecuta: pip install -r requirements.txt")
        print("   3. Ejecuta: python manage.py migrate")
        print("   4. Consulta INSTALACION.md para más ayuda\n")
        return False
    else:
        print("\n🎉 ¡TODO ESTÁ CORRECTAMENTE INSTALADO! 🎉")
        print("\nPróximos pasos:")
        print("   1. Ejecuta: python manage.py runserver")
        print("   2. Visita: http://127.0.0.1:8000/api/docs/")
        print("   3. Ejecuta las pruebas: python tests/test_apis_mock_completo.py\n")
        return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Verificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {str(e)}")
        sys.exit(1)
