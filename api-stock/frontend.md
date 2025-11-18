# Requerimientos para el Frontend - Sistema de Gestión de Stock

Este documento detalla los requerimientos funcionales y no funcionales para la aplicación frontend del Sistema de Gestión de Stock.

## 1. Objetivo del Proyecto

Desarrollar una interfaz de usuario web, moderna y reactiva que consuma la API de gestión de stock existente. La aplicación permitirá a los usuarios administrar productos, categorías y reservas de manera eficiente.

## 2. Stack Tecnológico

- **Framework:** Next.js
- **Lenguaje:** TypeScript
- **UI Kit:** shadcn/ui
- **Estilos:** Tailwind CSS

## 3. Módulos y Funcionalidades

A continuación se desglosan las funcionalidades por cada módulo de la aplicación, basadas en los endpoints de la API existente.

### 3.1. Módulo de Productos

- [ ] **Listado de Productos:**
    - [ ] Visualizar productos en una tabla o cuadrícula.
    - [ ] Implementar paginación para navegar entre los resultados.
    - [ ] Campo de búsqueda para filtrar productos por nombre.
    - [ ] Menú desplegable para filtrar productos por categoría.
- [ ] **Detalle de Producto:**
    - [ ] Página dedicada para ver todos los detalles de un producto, incluyendo imágenes.
- [ ] **Crear Producto:**
    - [ ] Formulario con validaciones para ingresar los datos de un nuevo producto.
    - [ ] Capacidad para subir una o más imágenes.
- [ ] **Actualizar Producto:**
    - [ ] Formulario pre-poblado con los datos del producto para su edición.
- [ ] **Eliminar Producto:**
    - [ ] Botón para desactivar un producto (borrado lógico).
    - [ ] Modal de confirmación antes de la eliminación.

### 3.2. Módulo de Categorías

- [ ] **Listado de Categorías:**
    - [ ] Visualizar todas las categorías activas en una lista o tabla.
- [ ] **Crear Categoría:**
    - [ ] Formulario simple para añadir una nueva categoría.
- [ ] **Actualizar Categoría:**
    - [ ] Edición en línea o mediante un modal para cambiar el nombre de la categoría.
- [ ] **Eliminar Categoría:**
    - [ ] Botón para desactivar una categoría.
    - [ ] Modal de confirmación.

### 3.3. Módulo de Reservas

- [ ] **Crear Reserva:**
    - [ ] Interfaz para seleccionar múltiples productos y especificar las cantidades a reservar.
    - [ ] Resumen de la reserva antes de confirmar.
- [ ] **Consultar Reserva:**
    - [ ] Campo de entrada para buscar una reserva por su ID y ver su estado y detalles.
- [ ] **Liberar Reserva:**
    - [ ] Interfaz para liberar el stock de una reserva existente, requiriendo el ID de la reserva.

## 4. Autenticación (Futuro)

- [ ] Aunque el backend no tiene la autenticación implementada, se debe diseñar la estructura de rutas pensando en el futuro:
    - [ ] Página de Login.
    - [ ] Rutas protegidas que requieran autenticación para acceder.
    - [ ] Rutas públicas.

## 5. Requerimientos de UI/UX

- [ ] **Diseño General:** Se debe seguir un layout de tipo "Dashboard" o panel de administración, con una barra de navegación lateral (sidebar) para acceder a los diferentes módulos.
- [ ] **Responsividad:** La aplicación debe ser completamente funcional y visualmente agradable en dispositivos de escritorio y tablets.
- [ ] **Notificaciones:** Implementar un sistema de notificaciones (toasts/snackbars) para dar feedback al usuario sobre el resultado de sus acciones (e.g., "Producto creado con éxito", "Error al actualizar la categoría").

## 6. Requerimientos No Funcionales

- [ ] **Manejo de Errores:** Mostrar mensajes de error claros y descriptivos cuando la API devuelva un error.
- [ ] **Rendimiento:** Optimizar la carga de imágenes y el renderizado de listas para asegurar una experiencia de usuario fluida.

## 7. Estructura de Carpetas Propuesta

A continuación se presenta una estructura de carpetas recomendada para organizar el código fuente del frontend, siguiendo las convenciones de Next.js (App Router) y los requerimientos del proyecto.

```
src/
|-- app/
|   |-- (pages)/
|   |   |-- products/
|   |   |   |-- page.tsx               # Página de listado de productos
|   |   |   |-- new/page.tsx           # Página para crear nuevo producto
|   |   |   `-- [id]/
|   |   |       |-- page.tsx           # Página de detalle de producto
|   |   |       `-- edit/page.tsx      # Página para editar producto
|   |   |-- categories/
|   |   |   `-- page.tsx               # Página para listar y gestionar categorías
|   |   `-- reservations/
|   |       `-- page.tsx               # Página para crear y consultar reservas
|   |-- layout.tsx                     # Layout principal de la aplicación
|   `-- page.tsx                       # Página de inicio o dashboard principal
|
|-- components/
|   |-- ui/                            # Componentes de shadcn/ui (auto-generados)
|   |-- shared/                        # Componentes reutilizables propios (Sidebar, Header, etc.)
|   `-- forms/                         # Formularios complejos (ProductForm, etc.)
|
|-- lib/
|   |-- api.ts                         # Funciones para interactuar con la API del backend
|   |-- definitions.ts                 # Definiciones de tipos y esquemas (TypeScript/Zod)
|   |-- hooks.ts                       # Hooks de React personalizados
|   `-- utils.ts                       # Funciones de utilidad (generado por shadcn)
|
`-- styles/
    `-- globals.css                    # Estilos globales
```

**Explicación:**
-   `app/`: Contiene todas las rutas y layouts de la aplicación, utilizando el App Router de Next.js. El grupo `(pages)` organiza las rutas de las funcionalidades principales sin afectar la URL.
-   `components/`: Alberga los componentes de React. Se divide en `ui` para los componentes de la librería shadcn/ui, `shared` para componentes propios que se usan en varias páginas, y `forms` para los formularios más complejos.
-   `lib/`: Contiene la lógica de negocio, funciones de acceso a datos, tipos y utilidades que no son componentes de React.
