from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from apps.apis.pedidoApi.models import Pedido


# =======================
#   Función auxiliar
# =======================
def _dashboard_context():
    """
    Devuelve datos reales de pedidos desde PostgreSQL.
    """
    # Obtener últimos 3 pedidos ordenados por fecha de creación
    ultimos_pedidos = Pedido.objects.select_related('usuario').order_by('-creado_en')[:3]
    
    # Mapear estados a formato esperado por el template
    estado_map = {
        'borrador': 'PENDIENTE',
        'pendiente': 'PENDIENTE',
        'confirmado': 'CONFIRMADO',
        'cancelado': 'CANCELADO',
    }
    
    transacciones = []
    for pedido in ultimos_pedidos:
        transacciones.append({
            "id": pedido.id,
            "usuario": pedido.usuario.username if pedido.usuario else "Anónimo",
            "monto": f"{pedido.total:,.2f}",
            "fecha": pedido.creado_en,
            "estado": estado_map.get(pedido.estado, 'PENDIENTE'),
        })
    
    # Calcular KPIs desde la base de datos
    total_pedidos = Pedido.objects.count()
    pedidos_confirmados = Pedido.objects.filter(estado='confirmado').count()
    ingresos_totales = sum(p.total for p in Pedido.objects.filter(estado='confirmado'))
    
    return {
        "kpi_ingresos": f"{ingresos_totales:,.0f}",
        "kpi_usuarios_nuevos": 42,  # Puedes calcular esto desde User.objects si quieres
        "kpi_items": total_pedidos,
        "kpi_ordenes_ok": pedidos_confirmados,
        "ultimas_transacciones": transacciones,
    }


# =======================
#   Vistas principales
# =======================

def administracion_view(request):
    """
    Vista principal del panel de administración.
    Muestra el menú para seleccionar entre Stock, Logística o Compras.
    """
    # Si querés exigir login, descomentá esto:
    # if not request.user.is_authenticated:
    #     return redirect('login')

    return render(request, 'admin_menu_principal.html')


def admin_stock_view(request):
    """
    Vista del panel de administración de Stock.
    """
    ctx = _dashboard_context()
    ctx['titulo'] = 'Administración de Stock'
    ctx['modulo'] = 'stock'
    return render(request, 'inicio_admin.html', ctx)


def admin_logistica_view(request):
    """
    Vista del panel de administración de Logística.
    """
    ctx = _dashboard_context()
    ctx['titulo'] = 'Administración de Logística'
    ctx['modulo'] = 'logistica'
    return render(request, 'inicio_admin.html', ctx)


def admin_compras_view(request):
    """
    Vista del panel de administración de Compras.
    """
    ctx = _dashboard_context()
    ctx['titulo'] = 'Administración de Compras'
    ctx['modulo'] = 'compras'
    return render(request, 'inicio_admin.html', ctx)


# =======================
#   Placeholders (para que no tire NoReverseMatch)
# =======================

def admin_items_nuevo(request):
    """
    Placeholder de 'Nuevo ítem'. 
    Más adelante reemplazalo por tu formulario real.
    """
    ctx = _dashboard_context()
    return render(request, 'inicio_admin.html', ctx)


def admin_reportes(request):
    """
    Placeholder de Reportes.
    """
    ctx = _dashboard_context()
    return render(request, 'inicio_admin.html', ctx)


def admin_config(request):
    """
    Placeholder de Configuración.
    """
    ctx = _dashboard_context()
    return render(request, 'inicio_admin.html', ctx)


def admin_transacciones(request):
    """
    Placeholder de Transacciones.
    """
    ctx = _dashboard_context()
    return render(request, 'inicio_admin.html', ctx)

