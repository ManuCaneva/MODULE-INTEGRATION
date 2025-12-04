"""
Script de prueba completo para las APIs Mock de Stock y Logística
Prueba el flujo E2E: Listar → Reservar → Calcular Costo → Crear Envío → Verificar
"""
import requests
from datetime import datetime
import json


class Colors:
    """Colores para terminal"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Imprime un encabezado con estilo"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")


def print_success(text):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    """Imprime mensaje de error"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text):
    """Imprime mensaje informativo"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def print_warning(text):
    """Imprime mensaje de advertencia"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def test_stock_api():
    """Prueba la API Mock de Stock"""
    print_header("PROBANDO API MOCK DE STOCK")
    
    BASE_URL = "http://127.0.0.1:8000/api/mock/stock"
    resultados = {
        'exitosos': 0,
        'fallidos': 0,
        'total': 0
    }
    
    # Test 1: Listar productos
    print(f"\n{Colors.BOLD}Test 1: Listar Productos{Colors.END}")
    try:
        response = requests.get(f"{BASE_URL}/productos/", params={'page': 1, 'limit': 5})
        if response.status_code == 200:
            productos = response.json()
            if productos and 'data' in productos:
                print_success(f"Productos obtenidos: {len(productos['data'])}")
                print_info(f"Total de productos: {productos['pagination']['total']}")
                resultados['exitosos'] += 1
            else:
                print_error("No se obtuvieron productos")
                resultados['fallidos'] += 1
        else:
            print_error(f"Error HTTP {response.status_code}")
            resultados['fallidos'] += 1
    except Exception as e:
        print_error(f"Error al listar productos: {str(e)}")
        resultados['fallidos'] += 1
    resultados['total'] += 1
    
    # Test 2: Obtener producto específico
    print(f"\n{Colors.BOLD}Test 2: Obtener Producto Específico (ID: 1){Colors.END}")
    try:
        response = requests.get(f"{BASE_URL}/1/producto/")
        if response.status_code == 200:
            producto = response.json()
            print_success(f"Producto obtenido: {producto.get('nombre', 'N/A')}")
            print_info(f"Precio: ${producto.get('precio', 0)}")
            print_info(f"Stock disponible: {producto.get('stock_disponible', 0)}")
            resultados['exitosos'] += 1
        else:
            print_error(f"Error HTTP {response.status_code}")
            resultados['fallidos'] += 1
    except Exception as e:
        print_error(f"Error al obtener producto: {str(e)}")
        resultados['fallidos'] += 1
    resultados['total'] += 1
    
    # Test 3: Listar categorías
    print(f"\n{Colors.BOLD}Test 3: Listar Categorías{Colors.END}")
    try:
        response = requests.get(f"{BASE_URL}/categorias/")
        if response.status_code == 200:
            categorias = response.json()
            if categorias and 'data' in categorias:
                print_success(f"Categorías obtenidas: {len(categorias['data'])}")
                for cat in categorias['data'][:3]:
                    print_info(f"  - {cat.get('nombre', 'N/A')}")
                resultados['exitosos'] += 1
            else:
                print_error("No se obtuvieron categorías")
                resultados['fallidos'] += 1
        else:
            print_error(f"Error HTTP {response.status_code}")
            resultados['fallidos'] += 1
    except Exception as e:
        print_error(f"Error al listar categorías: {str(e)}")
        resultados['fallidos'] += 1
    resultados['total'] += 1
    
    # Test 4: Reservar stock
    print(f"\n{Colors.BOLD}Test 4: Reservar Stock{Colors.END}")
    id_compra = f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    try:
        payload = {
            "idCompra": id_compra,
            "usuarioId": 999,
            "productos": [
                {"idProducto": 1, "cantidad": 2},
                {"idProducto": 3, "cantidad": 1}
            ]
        }
        response = requests.post(f"{BASE_URL}/reservar/", json=payload)
        if response.status_code in [200, 201]:
            reserva = response.json()
            print_success(f"Reserva creada exitosamente")
            print_info(f"ID Reserva: {reserva['idReserva']}")
            print_info(f"Estado: {reserva.get('estado', 'N/A')}")
            print_info(f"ID Compra: {id_compra}")
            resultados['exitosos'] += 1
        else:
            print_error(f"Error HTTP {response.status_code}: {response.text}")
            resultados['fallidos'] += 1
    except Exception as e:
        print_error(f"Error al reservar stock: {str(e)}")
        resultados['fallidos'] += 1
    resultados['total'] += 1
    
    # Test 5: Listar reservas
    print(f"\n{Colors.BOLD}Test 5: Listar Reservas del Usuario{Colors.END}")
    try:
        response = requests.get(f"{BASE_URL}/reservas/", params={'usuarioId': 999, 'page': 1, 'limit': 10})
        if response.status_code == 200:
            reservas = response.json()
            if reservas and 'data' in reservas:
                print_success(f"Reservas del usuario: {len(reservas['data'])}")
                print_info(f"Total de reservas: {reservas['pagination']['total']}")
                resultados['exitosos'] += 1
            else:
                print_error("No se obtuvieron reservas")
                resultados['fallidos'] += 1
        else:
            print_error(f"Error HTTP {response.status_code}")
            resultados['fallidos'] += 1
    except Exception as e:
        print_error(f"Error al listar reservas: {str(e)}")
        resultados['fallidos'] += 1
    resultados['total'] += 1
    
    # Resumen
    print(f"\n{Colors.BOLD}{'─'*70}{Colors.END}")
    print(f"{Colors.BOLD}Resumen Stock API:{Colors.END}")
    print(f"  Total tests: {resultados['total']}")
    print_success(f"  Exitosos: {resultados['exitosos']}")
    if resultados['fallidos'] > 0:
        print_error(f"  Fallidos: {resultados['fallidos']}")
    
    return resultados


def test_logistica_api():
    """Prueba la API Mock de Logística"""
    print_header("PROBANDO API MOCK DE LOGÍSTICA")
    
    BASE_URL = "http://127.0.0.1:8000/api/mock/logistica"
    resultados = {
        'exitosos': 0,
        'fallidos': 0,
        'total': 0
    }
    
    # Test 1: Obtener métodos de transporte
    print(f"\n{Colors.BOLD}Test 1: Métodos de Transporte{Colors.END}")
    try:
        response = requests.get(f"{BASE_URL}/shipping/transport-methods/")
        if response.status_code == 200:
            metodos = response.json()
            if metodos and 'data' in metodos:
                print_success(f"Métodos obtenidos: {len(metodos['data'])}")
                for metodo in metodos['data']:
                    print_info(f"  - {metodo.get('nombre_display', 'N/A')} ({metodo.get('tipo', 'N/A')})")
                resultados['exitosos'] += 1
            else:
                print_error("No se obtuvieron métodos de transporte")
                resultados['fallidos'] += 1
        else:
            print_error(f"Error HTTP {response.status_code}")
            resultados['fallidos'] += 1
    except Exception as e:
        print_error(f"Error al obtener métodos: {str(e)}")
        resultados['fallidos'] += 1
    resultados['total'] += 1
    
    # Test 2: Calcular costo de envío
    print(f"\n{Colors.BOLD}Test 2: Calcular Costo de Envío{Colors.END}")
    direccion = {
        "street": "Av. Corrientes 1234",
        "city": "Buenos Aires",
        "state": "CABA",
        "postal_code": "C1043",
        "country": "Argentina"
    }
    productos = [
        {"id": 1, "quantity": 2},
        {"id": 3, "quantity": 1}
    ]
    
    try:
        payload = {
            "delivery_address": direccion,
            "products": productos,
            "transport_type": "road"
        }
        response = requests.post(f"{BASE_URL}/shipping/cost/", json=payload)
        if response.status_code == 200:
            costo = response.json()
            print_success(f"Costo calculado: ${costo['estimated_cost']}")
            print_info(f"Tipo transporte: {costo.get('transport_type', 'N/A')}")
            print_info(f"Días estimados: {costo.get('estimated_delivery_days', 'N/A')}")
            resultados['exitosos'] += 1
        else:
            print_error(f"Error HTTP {response.status_code}: {response.text}")
            resultados['fallidos'] += 1
    except Exception as e:
        print_error(f"Error al calcular costo: {str(e)}")
        resultados['fallidos'] += 1
    resultados['total'] += 1
    
    # Test 3: Crear envío
    print(f"\n{Colors.BOLD}Test 3: Crear Envío{Colors.END}")
    try:
        envio_data = {
            "order_id": 1001,
            "user_id": 999,
            "delivery_address": direccion,
            "transport_type": "road",
            "products": productos
        }
        
        response = requests.post(f"{BASE_URL}/shipping/", json=envio_data)
        if response.status_code == 201:
            envio = response.json()
            print_success(f"Envío creado exitosamente")
            print_info(f"ID Envío: {envio['shipping_id']}")
            print_info(f"Tracking: {envio.get('tracking_number', 'N/A')}")
            print_info(f"Estado: {envio.get('estado', 'N/A')}")
            resultados['exitosos'] += 1
        else:
            print_error(f"Error HTTP {response.status_code}: {response.text}")
            resultados['fallidos'] += 1
    except Exception as e:
        print_error(f"Error al crear envío: {str(e)}")
        resultados['fallidos'] += 1
    resultados['total'] += 1
    
    # Test 4: Listar envíos
    print(f"\n{Colors.BOLD}Test 4: Listar Envíos del Usuario{Colors.END}")
    try:
        response = requests.get(f"{BASE_URL}/shipping/", params={'user_id': 999, 'page': 1, 'limit': 10})
        if response.status_code == 200:
            envios = response.json()
            if envios and 'data' in envios:
                print_success(f"Envíos del usuario: {len(envios['data'])}")
                print_info(f"Total de envíos: {envios['pagination']['total']}")
                resultados['exitosos'] += 1
            else:
                print_error("No se obtuvieron envíos")
                resultados['fallidos'] += 1
        else:
            print_error(f"Error HTTP {response.status_code}")
            resultados['fallidos'] += 1
    except Exception as e:
        print_error(f"Error al listar envíos: {str(e)}")
        resultados['fallidos'] += 1
    resultados['total'] += 1
    
    # Resumen
    print(f"\n{Colors.BOLD}{'─'*70}{Colors.END}")
    print(f"{Colors.BOLD}Resumen Logística API:{Colors.END}")
    print(f"  Total tests: {resultados['total']}")
    print_success(f"  Exitosos: {resultados['exitosos']}")
    if resultados['fallidos'] > 0:
        print_error(f"  Fallidos: {resultados['fallidos']}")
    
    return resultados
    
    # Resumen
    print(f"\n{Colors.BOLD}{'─'*70}{Colors.END}")
    print(f"{Colors.BOLD}Resumen Logística API:{Colors.END}")
    print(f"  Total tests: {resultados['total']}")
    print_success(f"  Exitosos: {resultados['exitosos']}")
    if resultados['fallidos'] > 0:
        print_error(f"  Fallidos: {resultados['fallidos']}")
    
    return resultados


def test_flujo_completo():
    """Prueba el flujo completo E2E"""
    print_header("FLUJO COMPLETO E2E: COMPRA → RESERVA → ENVÍO")
    
    STOCK_URL = "http://127.0.0.1:8000/api/mock/stock"
    LOGISTICA_URL = "http://127.0.0.1:8000/api/mock/logistica"
    
    print(f"{Colors.BOLD}Escenario: Usuario compra 2 productos y solicita envío{Colors.END}\n")
    
    # Paso 1: Buscar productos disponibles
    print(f"{Colors.BOLD}Paso 1: Buscar productos con stock{Colors.END}")
    try:
        response = requests.get(f"{STOCK_URL}/productos/", params={'page': 1, 'limit': 10})
        if response.status_code == 200:
            productos = response.json()
            productos_disponibles = [p for p in productos['data'] if p['stock_disponible'] > 0]
            print_success(f"Productos disponibles: {len(productos_disponibles)}")
            
            producto1 = productos_disponibles[0]
            producto2 = productos_disponibles[1] if len(productos_disponibles) > 1 else productos_disponibles[0]
            
            print_info(f"Producto 1: {producto1['nombre']} - Stock: {producto1['stock_disponible']}")
            print_info(f"Producto 2: {producto2['nombre']} - Stock: {producto2['stock_disponible']}")
        else:
            print_error(f"Error al buscar productos: HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error al buscar productos: {str(e)}")
        return False
    
    # Paso 2: Reservar stock
    print(f"\n{Colors.BOLD}Paso 2: Reservar stock de productos{Colors.END}")
    id_compra = f"ORDER-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    try:
        payload = {
            "idCompra": id_compra,
            "usuarioId": 888,
            "productos": [
                {"idProducto": producto1['id'], "cantidad": 1},
                {"idProducto": producto2['id'], "cantidad": 1}
            ]
        }
        response = requests.post(f"{STOCK_URL}/reservar/", json=payload)
        if response.status_code in [200, 201]:
            reserva = response.json()
            print_success(f"Stock reservado - ID Reserva: {reserva['idReserva']}")
            print_info(f"ID Compra: {id_compra}")
        else:
            print_error(f"Error al reservar stock: HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error al reservar stock: {str(e)}")
        return False
    
    # Paso 3: Calcular costo de envío
    print(f"\n{Colors.BOLD}Paso 3: Calcular costo de envío{Colors.END}")
    direccion = {
        "street": "Av. Libertador 5000",
        "city": "Buenos Aires",
        "state": "CABA",
        "postal_code": "C1426",
        "country": "Argentina"
    }
    try:
        payload = {
            "delivery_address": direccion,
            "products": [
                {"id": producto1['id'], "quantity": 1},
                {"id": producto2['id'], "quantity": 1}
            ],
            "transport_type": "road"
        }
        response = requests.post(f"{LOGISTICA_URL}/shipping/cost/", json=payload)
        if response.status_code == 200:
            costo = response.json()
            print_success(f"Costo calculado: ${costo['estimated_cost']}")
            print_info(f"Entrega estimada: {costo['estimated_delivery_days']} días")
        else:
            print_error(f"Error al calcular costo: HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error al calcular costo: {str(e)}")
        return False
    
    # Paso 4: Crear envío
    print(f"\n{Colors.BOLD}Paso 4: Crear envío{Colors.END}")
    try:
        envio_data = {
            "order_id": reserva['idReserva'],
            "user_id": 888,
            "delivery_address": direccion,
            "transport_type": "road",
            "products": [
                {"id": producto1['id'], "quantity": 1},
                {"id": producto2['id'], "quantity": 1}
            ]
        }
        response = requests.post(f"{LOGISTICA_URL}/shipping/", json=envio_data)
        if response.status_code == 201:
            envio = response.json()
            print_success(f"Envío creado - ID: {envio['shipping_id']}")
            print_info(f"Tracking: {envio['tracking_number']}")
            print_info(f"Costo: ${envio['costo_envio']}")
        else:
            print_error(f"Error al crear envío: HTTP {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error al crear envío: {str(e)}")
        return False
    
    # Paso 5: Verificar reserva y envío
    print(f"\n{Colors.BOLD}Paso 5: Verificar estado final{Colors.END}")
    try:
        response = requests.get(f"{STOCK_URL}/reservas/{reserva['idReserva']}/", params={'usuarioId': 888})
        if response.status_code == 200:
            reserva_detalle = response.json()
            print_success(f"Reserva confirmada - Estado: {reserva_detalle['estado']}")
        
        response = requests.get(f"{LOGISTICA_URL}/shipping/{envio['shipping_id']}/")
        if response.status_code == 200:
            envio_detalle = response.json()
            print_success(f"Envío confirmado - Estado: {envio_detalle['estado']}")
    except Exception as e:
        print_warning(f"No se pudo verificar estado: {str(e)}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ FLUJO COMPLETO EXITOSO{Colors.END}\n")
    return True


def main():
    """Función principal"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║         SCRIPT DE PRUEBA - APIs Mock Stock y Logística           ║")
    print("║                     Proyecto: DesarrolloAPP                       ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    print_info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Stock API: http://127.0.0.1:8000/api/mock/stock")
    print_info(f"Logística API: http://127.0.0.1:8000/api/mock/logistica")
    
    # Ejecutar tests
    resultados_stock = test_stock_api()
    resultados_logistica = test_logistica_api()
    flujo_exitoso = test_flujo_completo()
    
    # Resumen final
    print_header("RESUMEN FINAL")
    
    total_tests = resultados_stock['total'] + resultados_logistica['total'] + (1 if flujo_exitoso else 0)
    total_exitosos = resultados_stock['exitosos'] + resultados_logistica['exitosos'] + (1 if flujo_exitoso else 0)
    total_fallidos = resultados_stock['fallidos'] + resultados_logistica['fallidos'] + (0 if flujo_exitoso else 1)
    
    print(f"{Colors.BOLD}Total de pruebas ejecutadas: {total_tests}{Colors.END}")
    print_success(f"Pruebas exitosas: {total_exitosos}")
    if total_fallidos > 0:
        print_error(f"Pruebas fallidas: {total_fallidos}")
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ¡TODAS LAS PRUEBAS PASARON! 🎉{Colors.END}\n")
    
    porcentaje = (total_exitosos / total_tests * 100) if total_tests > 0 else 0
    print(f"\n{Colors.BOLD}Tasa de éxito: {porcentaje:.1f}%{Colors.END}\n")


if __name__ == "__main__":
    main()
