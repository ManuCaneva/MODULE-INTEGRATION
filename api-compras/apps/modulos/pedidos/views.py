from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.shortcuts import render, redirect
from django.urls import reverse
from Main.settings import build_prefixed_path
from django.db.models import Count
from .models import Pedido, DetallePedido
from django.http import JsonResponse
from django.conf import settings
import logging
import traceback

# module logger
logger = logging.getLogger(__name__)

# Esta vista parece ser de otra app, pero la dejamos por si acaso.
# Si no pertenece aquí, podés moverla a la app correspondiente.
def inicio_view(request):
    context = {
        'categorias_destacadas': "prueba",
        'productos_destacados': "prueba",
    }
    return render(request, 'inicio.html', context)


def checkout_view(request):
    """Pantalla de checkout para los pedidos."""
    from utils.apiCliente.logistica import LogisticsClient
    from utils.apiCliente.base import APIError
    from utils.keycloak import get_service_token_provider
    
    tipos_envio = []
    
    # Intentar obtener métodos de transporte desde la API de Logística
    try:
        log_client = LogisticsClient(
            settings.LOGISTICA_API_BASE_URL,
            token_provider=get_service_token_provider()
        )
        response = log_client.get_transport_methods()
        
        # La API devuelve: {"transportMethods": [{"id": 1, "name": "Air Transport", "type": "air", "estimatedDays": "1-3"}, ...]}
        metodos = response.get('transportMethods', [])
        
        # Mapeo de íconos para cada tipo de transporte
        iconos_transporte = {
            'air': '✈️',
            'sea': '🚢',
            'road': '🚚',
            'rail': '🚆',
        }
        
        for metodo in metodos:
            transport_type = metodo.get('type', 'road')
            estimated_days = metodo.get('estimatedDays', 'A confirmar')
            
            tipos_envio.append({
                "id": transport_type,
                "nombre": metodo.get('name', f'Envío {transport_type}'),
                "descripcion": f"Entrega estimada en {estimated_days} días.",
                "costo": "A calcular en checkout",
                "dias_estimados": estimated_days,
                "icono": iconos_transporte.get(transport_type, '📦'),
            })
            
        logger.info(f"Métodos de transporte obtenidos desde API: {len(tipos_envio)}")
        
    except APIError as e:
        logger.warning(f"No se pudieron obtener métodos de transporte de la API: {e}")
        # Fallback a métodos básicos si falla la API
       
    except Exception as e:
        logger.exception(f"Error inesperado al obtener métodos de transporte: {e}")
        # Fallback a método básico en caso de error inesperado
        tipos_envio = [
            {
                "id": "road",
                "nombre": "Envío estándar",
                "descripcion": "Entrega en 2-5 días hábiles.",
                "costo": "A calcular",
                "dias_estimados": "2-5",
                "icono": "🚚",
            },
        ]

    context = {
        "tipos_envio": tipos_envio,
        "checkout_endpoint": build_prefixed_path("/api/shopcart/checkout"),
        "api_base": build_prefixed_path("/api").rstrip("/"),
        "success_url": reverse("pedidos:pago_exitoso"),
        "failure_url": reverse("pedidos:pago_fallido"),
    }
    return render(request, "checkout.html", context)

# @login_required
# views.py
from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import render, redirect
from .models import Pedido, DetallePedido

# @login_required
def listar_pedidos(request):
    """
    Muestra una lista de pedidos. En desarrollo, permite sembrar datos de prueba con ?seed=1.
    """
    # Sembrar datos "hardcodeados" en la BD si estamos en DEBUG y llegan con ?seed=1
    if settings.DEBUG and request.GET.get("seed") == "1":
        _seed_demo_pedidos(request.user) # Pasamos el usuario para asociar el pedido
        return redirect(request.path)

    # CAMBIO: el campo es 'usuario' y la fecha es 'creado_en'
    pedidos_base = Pedido.objects.filter(usuario=request.user).order_by('-creado_en')
    estado_solicitado = request.GET.get('estado')
    # CAMBIO: los estados válidos vienen de Pedido.Estado.choices
    estados_validos = {choice[0]: choice[1] for choice in Pedido.Estado.choices}

    if estado_solicitado not in estados_validos:
        estado_solicitado = None

    pedidos = pedidos_base
    if estado_solicitado:
        pedidos = pedidos.filter(estado=estado_solicitado)

    resumen_estados = {clave: 0 for clave in estados_validos.keys()}
    for item in pedidos_base.values('estado').annotate(total=Count('id')):
        resumen_estados[item['estado']] = item['total']
    
    filtros_estado = [
        {
            'clave': clave,
            'etiqueta': estados_validos[clave],
            'cantidad': resumen_estados.get(clave, 0),
        }
        for clave in estados_validos
    ]

    context = {
        'pedidos': pedidos,
        'filtros_estado': filtros_estado,
        'estado_solicitado': estado_solicitado,
        'total_pedidos': pedidos_base.count(),
        'etiqueta_estado': estados_validos.get(estado_solicitado) if estado_solicitado else None,
    }
    return render(request, 'pedidos/listar_pedidos.html', context)


# ✅ NUEVA VISTA PARA LA PANTALLA DE PAGO EXITOSO
#@login_required   <-- Lo dejamos comentado por ahora para poder probarlo
def pago_exitoso(request):
    """
    Muestra la página de confirmación de pago exitoso.
    """
    return render(request, 'pedidos/pago_exitoso.html')

# ✅ NUEVA VISTA PARA LA PANTALLA DE PAGO FALLIDO
# @login_required  <-- Lo dejamos comentado por ahora para poder probarlo
def pago_fallido(request):
    """
    Muestra la página de notificación de pago fallido.
    """
    return render(request, 'pedidos/pago_fallido.html')


def mis_pedidos(request):
    """
    Muestra el historial de pedidos del usuario.
    """
    from apps.apis.pedidoApi.serializer import PedidoSerializer
    
    pedidos = []
    logger.info(f"Usuario autenticado: {request.user.is_authenticated}, Usuario: {request.user}")
    
    if request.user.is_authenticated:
        # Obtener pedidos del usuario directamente del modelo
        pedidos_queryset = Pedido.objects.filter(usuario=request.user).select_related("direccion_envio").prefetch_related("detalles").order_by('-creado_en')
        logger.info(f"Pedidos encontrados: {pedidos_queryset.count()}")
        serializer = PedidoSerializer(pedidos_queryset, many=True, context={"request": request})
        pedidos = serializer.data
        logger.info(f"Pedidos serializados: {len(pedidos)}")
    else:
        logger.warning("Usuario no autenticado intentando ver pedidos")

    context = {
        'pedidos': pedidos,
    }
    return render(request, 'pedidos/mis_pedidos.html', context)


# --- FUNCIONES AUXILIARES PARA DATOS DE PRUEBA ---

def _ensure_demo_user():
    """Crea (o recupera) un usuario 'demo'."""
    User = get_user_model()
    demo_user, created = User.objects.get_or_create(
        username='demo',
        defaults={'email': 'demo@example.com'}
    )
    if created:
        # set_password para no guardar en texto plano
        demo_user.set_password('demo12345')
        demo_user.save()
    return demo_user
@transaction.atomic


@transaction.atomic
def _seed_demo_pedidos(user):
    """Crea datos de prueba (limpiando los anteriores de ese usuario)."""
    if user.username != 'demo':
        demo_user = user
    else:
        demo_user = _ensure_demo_user()

    Pedido.objects.filter(usuario=demo_user).delete()

    # Pedido 1
    p1 = Pedido.objects.create(usuario=demo_user, total=Decimal('45999.90'), estado='pendiente')
    DetallePedido.objects.create(pedido=p1, producto_id=1, nombre_producto='Remera Oversize Negra', cantidad=2, precio_unitario=Decimal('9999.95'))
    DetallePedido.objects.create(pedido=p1, producto_id=2, nombre_producto='Jean Slim Azul', cantidad=1, precio_unitario=Decimal('25999.00'))

    # Pedido 2
    p2 = Pedido.objects.create(usuario=demo_user, total=Decimal('18998.00'), estado='pendiente')
    DetallePedido.objects.create(pedido=p2, producto_id=3, nombre_producto='Buzo Canguro Gris', cantidad=1, precio_unitario=Decimal('12999.00'))
    DetallePedido.objects.create(pedido=p2, producto_id=4, nombre_producto='Medias Deportivas (Pack x3)', cantidad=1, precio_unitario=Decimal('5999.00'))
    
    # Pedido 3
    p3 = Pedido.objects.create(usuario=demo_user, total=Decimal('32999.00'), estado='pendiente')
    DetallePedido.objects.create(pedido=p3, producto_id=5, nombre_producto='Zapatillas Urbanas', cantidad=1, precio_unitario=Decimal('32999.00'))



@transaction.atomic
def api_checkout_confirm(request):
    # Este endpoint es una API: no usar el redirect del decorator `login_required`
    # para evitar errores de reverse a la vista de login cuando la petición es AJAX.
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    """Endpoint temporal para confirmar checkout: crear dirección, pedido, reservar stock y crear envío.

    POST JSON esperado (mínimo):
    {
      "deliveryAddress": { "nombre_receptor":..., "calle":..., "ciudad":..., "codigo_postal":..., "pais":..., "telefono":... },
      "products": [{"productId": 1, "quantity": 2}, ...],
      "transport_type": "road",
      "payment_method": "card",
      "idCompra": "opcional-idempotency"
    }

    Responde: JSON con detalles de pedido, reserva y envío o error.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        import json, uuid
        from decimal import Decimal as D
        from django.conf import settings
        from .models import DireccionEnvio
        from utils.apiCliente.stock import StockClient
        from utils.apiCliente.logistica import LogisticsClient
        from utils.apiCliente.base import APIError
        from utils.keycloak import get_service_token_provider
        payload = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        logger.exception('JSON inválido en checkout_confirm')
        return JsonResponse({'error': 'JSON inválido', 'detail': str(e)}, status=400)

    address = payload.get('deliveryAddress')
    products = payload.get('products') or []
    transport_type = payload.get('transport_type')
    id_compra = payload.get('idCompra') or str(uuid.uuid4())

    if not address or not products:
        return JsonResponse({'error': 'Faltan campos deliveryAddress o products'}, status=400)

    user = request.user
    stock_client = StockClient(settings.STOCK_API_BASE_URL)
    
    # Intentar obtener token del usuario (si existe) para Logística
    token_logistica = None
    try:
        from allauth.socialaccount.models import SocialToken
        social_token = SocialToken.objects.filter(account__user=user, account__provider='keycloak').first()
        if social_token:
            token_logistica = social_token.token
            logger.info(f"Usando token de usuario para Logística: {token_logistica[:10]}...")
    except Exception as e:
        logger.warning(f"No se pudo obtener token de usuario: {e}")

    # Si no hay token de usuario, usar token de servicio
    provider = None
    if token_logistica:
        provider = lambda: token_logistica
    else:
        try:
            srv_provider = get_service_token_provider(silent=False)
            token_srv = srv_provider()
            logger.info(f"Usando token de servicio para Logística: {token_srv[:10]}...")
            provider = lambda: token_srv
        except Exception as e:
            logger.error(f"Error obteniendo token de servicio: {e}")

    log_client = LogisticsClient(
        settings.LOGISTICA_API_BASE_URL,
        token_provider=provider
    )

    try:
        dir_envio = DireccionEnvio.objects.create(
            usuario=user,
            nombre_receptor=address.get('nombre_receptor') or f"{getattr(user,'first_name','')} {getattr(user,'last_name','')}",
            calle=address.get('calle',''),
            ciudad=address.get('ciudad',''),
            provincia=address.get('provincia',''),
            codigo_postal=address.get('codigo_postal',''),
            pais=address.get('pais','Argentina'),
            telefono=address.get('telefono',''),
            informacion_adicional=address.get('informacion_adicional',''),
        )

        pedido = Pedido.objects.create(usuario=user, direccion_envio=dir_envio, estado=Pedido.Estado.BORRADOR)

        total = D('0.00')
        for item in products:
            pid = int(item.get('productId'))
            qty = int(item.get('quantity') or 0)
            precio_unitario = D('0.00')
            prod = None
            try:
                candidate = stock_client.obtener_producto(pid)
                # asegurarnos de que recibimos un dict con los datos esperados
                if isinstance(candidate, dict):
                    prod = candidate
                    # Obtener precio de forma robusta: soportar keys 'price' o 'precio'
                    price_val = prod.get('price') or prod.get('precio') or '0.00'
                    precio_unitario = D(str(price_val))
                else:
                    # si el cliente devolvió un objeto inesperado (ej. MagicMock), lo ignoramos
                    raise ValueError('Producto no es dict')
            except Exception:
                logger.warning('No se pudo obtener precio para producto %s', pid)

            DetallePedido.objects.create(
                pedido=pedido,
                producto_id=pid,
                nombre_producto=(prod.get('name') if prod else f'Producto {pid}'),
                cantidad=qty,
                precio_unitario=precio_unitario,
            )
            total += precio_unitario * qty

        pedido.total = total
        pedido.save(update_fields=['total'])

        reserva_payload_products = [{'productId': int(i.get('productId')), 'quantity': int(i.get('quantity'))} for i in products]
        try:
            reserva_resp = stock_client.reservar_stock(id_compra, user.id, reserva_payload_products)
        except APIError as e:
            logger.exception('Reserva de stock fallida para compra %s', id_compra)
            return JsonResponse({'error': 'Reserva de stock fallida', 'detail': getattr(e,'payload',str(e))}, status=409)

        reserva_id = reserva_resp.get('id') or reserva_resp.get('reservationId') or str(reserva_resp)
        pedido.referencia_reserva_stock = str(reserva_id)
        pedido.save(update_fields=['referencia_reserva_stock'])

        try:
            delivery_payload = dir_envio.generar_datos_logistica()
            envio_resp = log_client.create_shipment(order_id=pedido.id, user_id=user.id, delivery_address=delivery_payload, transport_type=transport_type or '', products=reserva_payload_products)
        except APIError as e:
            logger.exception('Creación de envío fallida, intentando liberar reserva %s', reserva_id)
            try:
                try:
                    rid = int(reserva_id)
                except Exception:
                    rid = reserva_id
                stock_client.liberar_stock(rid, user.id, motivo='Compensación por fallo en logística')
            except Exception:
                logger.exception('Fallo liberando reserva %s', reserva_id)
            return JsonResponse({'error': 'Creación de envío fallida', 'detail': getattr(e,'payload',str(e))}, status=502)

        envio_id = envio_resp.get('id') or envio_resp.get('trackingId') or str(envio_resp)
        pedido.referencia_envio = str(envio_id)
        pedido.marcar_confirmado(referencia_envio=str(envio_id), referencia_reserva_stock=str(reserva_id))

        return JsonResponse({'pedido': {'id': pedido.id, 'estado': pedido.estado, 'total': str(pedido.total)}, 'reserva': reserva_resp, 'envio': envio_resp}, status=201)

    except Exception as e:
        logger.exception('Error inesperado en checkout_confirm')
        # En DEBUG devolvemos el traceback para facilitar debugging desde el frontend
        detail = str(e)
        if getattr(settings, 'DEBUG', False):
            detail = traceback.format_exc()
        return JsonResponse({'error': 'Error interno', 'detail': detail}, status=500)
