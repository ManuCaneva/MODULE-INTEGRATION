# inicio

Módulo principal del catálogo de productos. Presenta la interfaz de usuario para explorar, buscar y filtrar productos disponibles en la tienda, con paginación y sistema de filtros avanzado.

---

## 📁 Estructura de archivos

### **`views.py`**
Lógica principal del catálogo de productos:

#### **`normalize(text)` (función auxiliar)**
Normaliza texto para búsquedas insensibles a mayúsculas, tildes y caracteres especiales:

**Proceso de normalización**:
1. Convierte a string si no lo es
2. Elimina caracteres invisibles (NO-BREAK SPACE, ZERO WIDTH SPACE, etc.)
3. Convierte a minúsculas
4. Normaliza Unicode (NFD) y elimina marcas diacríticas (tildes)
5. Colapsa múltiples espacios en uno solo

**Ejemplo**:
```python
normalize("Remera Básica")  # → "remera basica"
normalize("PANTALÓN")       # → "pantalon"
normalize("  Múltiples   espacios  ")  # → "multiples espacios"
```

**Responsabilidad**: Garantizar búsquedas flexibles que ignoren diferencias de formato en texto.

---

#### **`inicio_view(request)`**
Vista principal del catálogo de productos con sistema completo de filtros y paginación:

**Parámetros GET aceptados**:
- `busqueda` / `q`: Término de búsqueda general (nombre o marca)
- `categoria`: Filtra por categoría exacta (normalizada)
- `marca`: Filtra por marca exacta (normalizada)
- `precio_minimo`: Precio mínimo (float)
- `precio_maximo`: Precio máximo (float)
- `page`: Número de página (default: 1)
- `limit`: Productos por página (default: 18)

**Flujo de ejecución**:

1. **Obtención de datos desde API**:
   - Instancia `ProductoAPIClient` con base URL `http://localhost:8000`
   - Llama a `listar_productos(page=1, limit=5000, search=termino_busqueda)`
   - **Estrategia**: Obtiene grandes cantidades de productos (hasta 5000) en una sola llamada para aplicar filtros localmente
   - Mide tiempo de respuesta con `perf_counter()` y lo registra en logs

2. **Normalización de productos**:
   - Procesa respuesta de la API (maneja formatos `{"data": [...]}` o listas directas)
   - Normaliza estructura de cada producto:
     - `id`: `id` o `pk`
     - `nombre`: `nombre` o `title`
     - `descripcion`: `descripcion` o `description`
     - `precio`: Convertido a float, default 0.0
     - `categoria`: Extrae de objeto anidado si existe (`categoria.nombre`) o usa string directo
     - `marca`: Campo `marca`
     - `imagen`: `imagen_url`, `imagen` o `imagenUrl`
   - Valida y castea tipos de datos para prevenir errores

3. **Extracción de opciones de filtros**:
   - Antes de filtrar, recopila todas las categorías únicas
   - Recopila todas las marcas únicas
   - Ordena alfabéticamente para los selectores

4. **Aplicación de filtros con normalización**:
   - Normaliza términos de búsqueda y filtros con `normalize()`
   - **Búsqueda general**: Coincidencia substring en nombre o marca (insensible a tildes/mayúsculas)
   - **Categoría**: Coincidencia exacta normalizada
   - **Marca**: Coincidencia exacta normalizada
   - **Rango de precio**: Filtrado numérico entre mínimo y máximo
   - Filtra todos los productos con función `_filtrar(prod)`

5. **Paginación manual**:
   - Calcula total de resultados después de filtrar
   - Determina total de páginas: `ceil(total / per_page)`
   - Valida número de página (entre 1 y total_pages)
   - Extrae slice de productos para página actual
   - Genera contexto de paginación con flags `has_next`, `has_prev`, `next_page`, `prev_page`

6. **Contexto de respuesta**:
   ```python
   {
       "productos": productos_pagina,  # 18 productos de la página actual
       "categorias": ["Remeras", "Pantalones", ...],  # Opciones de filtro
       "marcas": ["UrbanFit", "ProSport", ...],       # Opciones de filtro
       "filtros": {...},                              # Valores actuales de filtros
       "cantidad_resultados": 45,                     # Total después de filtrar
       "carrito": [],                                 # Carrito (vacío, legacy)
       "total_carrito": 0.0,                          # Total carrito (legacy)
       "pagination": {
           "total": 45,
           "per_page": 18,
           "current_page": 2,
           "total_pages": 3,
           "has_next": True,
           "has_prev": True,
           "next_page": 3,
           "prev_page": 1
       }
   }
   ```

7. **Logging detallado**:
   - Log de entrada: usuario, path completo
   - Log de API: tiempo de respuesta, cantidad de productos obtenidos
   - Log de filtros: parámetros aplicados y resultados
   - Log de errores: stack trace completo ante excepciones
   - Log de salida: cantidad de productos renderizados y paginación

**Manejo de errores**:
- Captura excepciones de la API y devuelve lista vacía de productos
- Valida conversión de tipos (page, limit, precios) con try/except
- Maneja respuestas None o formatos inesperados de la API

**Responsabilidad**: Controlador principal del catálogo. Orquesta obtención de datos, normalización, filtrado, paginación y renderizado. Implementa búsqueda flexible e insensible a formato de texto.

---

### **`models.py`**
Archivo vacío (sin modelos propios).

**Responsabilidad**: Este módulo no persiste datos localmente. Todos los productos se obtienen desde productoApi/Stock API en tiempo real.

---

### **`urls.py`**
Configuración de rutas del módulo:

**Rutas definidas**:
```python
path('', views.inicio_view, name='inicio')
# path('QR/', views.AnalisisQR, name='AnalizarQR')  # Comentado, no implementado
```

**URL base**: `/` (raíz del sitio)

**Responsabilidad**: Mapeo de la ruta raíz al catálogo de productos. Ruta principal del sitio web.

---

### **`templates/inicio.html`**
Template del catálogo de productos con filtros y paginación:

**Extiende**: `base.html` (layout principal del sitio)

**Estructura HTML**:

1. **Sidebar de filtros** (`.filters-sidebar`):
   - **Búsqueda por texto**: Input `busqueda` para nombre/marca
   - **Categoría**: Select con opciones dinámicas desde `categorias`
   - **Marca**: Select con opciones dinámicas desde `marcas`
   - **Rango de precio**: Inputs numéricos para `precio_minimo` y `precio_maximo`
   - **Botones de acción**:
     - "Aplicar": Submit del formulario con filtros
     - "Limpiar": Redirige a `/` sin parámetros
   - **Versión móvil**: Header con botón de cierre (`#close-filters-btn`)

2. **Grid de productos** (`.product-grid-container`):
   - **Header**:
     - Título "Productos"
     - Botón para abrir filtros en móvil (`#open-filters-btn`)
     - Contador de resultados: "X resultado(s)"
   - **Tarjetas de productos** (`.product-card`):
     - Atributos data: `data-id`, `data-nombre`, `data-precio`, `data-imagen`
     - Tag de categoría (`.category-tag`)
     - Imagen del producto
     - Información: marca, nombre, precio formateado
     - **Acciones**:
       - Botón "Agregar al Carrito" (`.add-to-cart-btn`)
       - Selector de cantidad (oculto por defecto, `.quantity-selector.hidden`)
       - Botones +/- para ajustar cantidad
       - Botón "Confirmar" (oculto, `.confirm-btn.hidden`)

3. **Sistema de paginación** (`.pagination-container`):
   - **Botón "Anterior"**: Si `pagination.has_prev`
   - **Números de página**: Loop generando enlaces del 1 al `total_pages`
     - Página activa con clase `.active`
     - Cada enlace preserva todos los filtros en query params
   - **Botón "Siguiente"**: Si `pagination.has_next`
   - **Preservación de filtros**: Todos los enlaces incluyen `busqueda`, `categoria`, `marca`, `precio_minimo`, `precio_maximo`

**Variables de contexto utilizadas**:
- `productos`: Lista de productos de la página actual (max 18)
- `categorias`: Lista de categorías disponibles (ordenadas)
- `marcas`: Lista de marcas disponibles (ordenadas)
- `filtros`: Dict con valores actuales de filtros
- `cantidad_resultados`: Total de productos después de filtrar
- `pagination`: Dict con info de paginación

**Estilos CSS**:
- Archivo específico: `css/apps/modulos/inicio/inicio.css`
- Clases utilizadas: `.shop-layout`, `.filters-sidebar`, `.product-grid`, `.product-card`, `.pagination-container`, etc.

**Interactividad JavaScript** (implícita):
- Apertura/cierre de sidebar de filtros en móvil
- Mostrar/ocultar selector de cantidad al hacer clic en "Agregar al Carrito"
- Incrementar/decrementar cantidad con botones +/-
- Confirmar y agregar producto al carrito

**Responsabilidad**: Presentación visual del catálogo con filtros avanzados, grid responsive y paginación. Interfaz principal de compra para usuarios.

---

### **`apps.py`**
Configuración de la aplicación Django:

```python
class ClienteStockConfig(AppConfig):
    name = 'apps.modulos.inicio'
    default_auto_field = 'django.db.models.BigAutoField'
```

**Nota**: El nombre de clase `ClienteStockConfig` no coincide con el módulo "inicio". Esto puede ser un residuo de refactoring.

**Responsabilidad**: Metadatos y configuración de la app para el registro en `INSTALLED_APPS`.

---

### **`admin.py`**
Archivo vacío (sin modelos registrados).

**Responsabilidad**: No hay gestión desde Django Admin ya que no hay modelos propios.

---

### **`tests.py`**
Archivo para pruebas (actualmente con imports básicos).

**Responsabilidad**: Testing del módulo. Debe contener pruebas para:
- Función `normalize()` con diferentes casos (tildes, mayúsculas, espacios)
- Vista `inicio_view()` sin filtros
- Filtros individuales (busqueda, categoria, marca, precio)
- Combinación de filtros
- Paginación (primera página, última página, página inválida)
- Manejo de errores de API
- Respuesta con productos vacíos

---

## 🔗 Dependencias externas

### **productoApi** (módulo interno)
- **Uso**: `ProductoAPIClient` para obtener productos
- **Método**: `listar_productos(page, limit, search)`
- **Estrategia**: Una llamada con `limit=5000` para filtrar localmente

### **Stock API** (módulo externo, a través de productoApi)
- **Endpoint**: `http://localhost:8000/api/product/`
- **Formato esperado**: 
  ```json
  {
    "data": [
      {
        "id": 1,
        "nombre": "Producto",
        "precio": 1000.0,
        "categoria": "Categoría" o {"nombre": "Categoría"},
        "marca": "Marca",
        "imagen_url": "/path/to/image"
      }
    ]
  }
  ```

---

## 🔧 Configuración requerida

En `Main/urls.py`:

```python
urlpatterns = [
    path('', include('apps.modulos.inicio.urls')),
    # ...
]
```

En `settings.py`:

```python
INSTALLED_APPS = [
    'apps.modulos.inicio',
    'apps.apis.productoApi',
    # ...
]

# Logging
LOGGING = {
    'loggers': {
        'apps.modulos.inicio': {
            'level': 'DEBUG',  # INFO en producción
            'handlers': ['console'],
        }
    }
}
```

CSS requerido:
- `static/css/apps/modulos/inicio/inicio.css` (estilos específicos del catálogo)

---

## 📊 Flujo de datos

### **Carga inicial del catálogo**:
```
Usuario → GET /
    ↓
inicio_view()
    ↓
ProductoAPIClient.listar_productos(page=1, limit=5000)
    ↓
Stock API → Devuelve ~90 productos
    ↓
Normaliza estructura de productos
    ↓
Extrae categorías y marcas únicas
    ↓
Pagina (productos 1-18)
    ↓
Renderiza inicio.html con productos + filtros + paginación
```

### **Aplicación de filtros**:
```
Usuario → Submit formulario filtros → GET /?busqueda=remera&categoria=Remeras&precio_minimo=5000
    ↓
inicio_view()
    ↓
Obtiene 5000 productos de API
    ↓
Normaliza términos de búsqueda: "remera" → "remera"
    ↓
Aplica filtros localmente:
  - busqueda in nombre OR busqueda in marca
  - categoria == "remeras" (normalizado)
  - precio >= 5000
    ↓
45 productos coinciden
    ↓
Pagina: 45 productos → 3 páginas de 18
    ↓
Renderiza página 1 con 18 productos
```

### **Navegación de paginación**:
```
Usuario → Click en "Página 2" → GET /?page=2&busqueda=remera&...
    ↓
inicio_view()
    ↓
Obtiene productos de API
    ↓
Aplica mismos filtros
    ↓
45 productos coinciden
    ↓
Extrae slice: productos[18:36]
    ↓
Renderiza página 2 con productos 19-36
```

---

## 🧪 Testing

Para ejecutar las pruebas del módulo:

```powershell
python manage.py test apps.modulos.inicio
```

Ejemplos de tests a implementar:

```python
class NormalizeTestCase(TestCase):
    def test_normalize_tildes(self):
        self.assertEqual(normalize("Remera básica"), "remera basica")
    
    def test_normalize_mayusculas(self):
        self.assertEqual(normalize("PANTALÓN"), "pantalon")
    
    def test_normalize_espacios(self):
        self.assertEqual(normalize("  múltiples   espacios  "), "multiples espacios")

class InicioViewTestCase(TestCase):
    def test_catalogo_sin_filtros(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('productos', response.context)
    
    def test_filtro_categoria(self):
        response = self.client.get('/?categoria=Remeras')
        productos = response.context['productos']
        for p in productos:
            self.assertEqual(normalize(p['categoria']), 'remeras')
    
    def test_paginacion(self):
        response = self.client.get('/?page=2')
        self.assertEqual(response.context['pagination']['current_page'], 2)
```

---

## 📝 Notas de implementación

1. **Estrategia de filtrado local vs remoto**:
   - Actualmente: Obtiene 5000 productos y filtra localmente
   - **Ventaja**: Mayor flexibilidad de filtros (normalización, rangos de precio)
   - **Desventaja**: Mayor carga de red y memoria
   - **Alternativa**: Delegar filtros a Stock API (requiere implementar endpoints específicos)

2. **Normalización de texto**:
   - Implementada con `unicodedata` para eliminar tildes
   - Crucial para UX: usuario busca "pantalón" y encuentra "pantalon"
   - Se aplica tanto a búsqueda como a filtros de categoría/marca

3. **Paginación con filtros**:
   - Todos los enlaces de paginación preservan filtros con `urlencode`
   - Cada cambio de página mantiene el contexto de búsqueda

4. **Logging extensivo**:
   - Nivel DEBUG: Parámetros de filtros, productos obtenidos
   - Nivel INFO: Tiempo de respuesta de API, productos renderizados
   - Nivel ERROR: Stack traces completos de excepciones
   - Útil para debugging de performance y errores de API

5. **Manejo robusto de errores**:
   - API devuelve None → Lista vacía
   - Precio inválido → 0.0
   - Página fuera de rango → Página 1 o última
   - Excepción de API → Lista vacía, no rompe la vista

6. **Legacy: carrito en contexto**:
   - `carrito` y `total_carrito` están en contexto pero vacíos
   - Probablemente legacy de implementación anterior
   - El carrito real se maneja por carritoApi con JavaScript/AJAX

7. **Límite de productos**: 
   - Hardcodeado `limit=5000` en llamada API
   - Si el catálogo crece, considerar paginación real desde API
   - Monitorear performance con `perf_counter()`

8. **Formato de respuesta flexible**:
   - Soporta `{"data": [...]}` y listas directas
   - Soporta múltiples nombres de campos: `id/pk`, `nombre/title`, `imagen_url/imagen/imagenUrl`
   - Maneja categorías como string o objeto `{"nombre": "..."}`

9. **Sin autenticación requerida**:
   - Vista pública, accesible sin login
   - Permite navegación anónima del catálogo

10. **Responsive con filtros móviles**:
    - Sidebar de filtros con botones de apertura/cierre para móviles
    - Grid adaptable con CSS flexbox/grid

---

## 🚀 Próximos pasos (optimizaciones futuras)

1. **Cache de productos**: Implementar cache de resultados de API con Redis/Memcached (TTL 5-10 minutos)

2. **Paginación real desde API**: Modificar para llamar solo la página solicitada:
   ```python
   resultado = client.listar_productos(page=page, limit=18, search=termino_busqueda)
   ```

3. **Filtros delegados a API**: Si Stock API soporta filtros, enviar `categoria`, `marca`, `precio_min`, `precio_max` en la llamada

4. **Lazy loading de imágenes**: Implementar `loading="lazy"` en tags `<img>` para mejorar performance

5. **Búsqueda con Elasticsearch**: Para catálogos grandes, indexar productos en Elasticsearch para búsquedas más rápidas

6. **Filtros persistentes en sesión**: Guardar filtros en sesión para restaurarlos entre navegaciones

7. **Ordenamiento**: Agregar opciones de ordenamiento (precio asc/desc, nombre, más vendidos)

8. **Vista de lista vs grid**: Toggle para cambiar entre vista de grilla y lista

9. **Favoritos**: Marcar productos favoritos con localStorage o cuenta de usuario

10. **Breadcrumbs**: Navegación contextual cuando se aplican filtros (Home > Remeras > UrbanFit)
