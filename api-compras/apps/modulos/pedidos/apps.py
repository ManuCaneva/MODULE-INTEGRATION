from django.apps import AppConfig


class PedidosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.modulos.pedidos'

    def ready(self):
        """Al iniciar la app, limpiar pedidos previos."""
        from django.db import connection
        from django.db.utils import OperationalError, ProgrammingError
        
        try:
            # Verificar si las tablas existen
            with connection.cursor() as cursor:
                from .models import Pedido
                
                # Comentado: No borrar pedidos en producción
                # Pedido.objects.all().delete()
                # print("✅ Pedidos limpios al reiniciar el servidor")
                pass
        except (OperationalError, ProgrammingError):
            # Las tablas aún no existen (ej. durante migraciones)
            pass
