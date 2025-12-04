document.addEventListener('DOMContentLoaded', () => {

    // --- LÓGICA PARA EL PANEL DE FILTROS RESPONSIVO ---
    const openFiltersBtn = document.getElementById('open-filters-btn');
    const closeFiltersBtn = document.getElementById('close-filters-btn');
    const filtersSidebar = document.getElementById('filters-sidebar');
    const filtersOverlay = document.getElementById('filters-overlay');

    function openFilters() {
        if (filtersSidebar) filtersSidebar.classList.add('open');
        if (filtersOverlay) filtersOverlay.classList.add('visible');
    }

    function closeFilters() {
        if (filtersSidebar) filtersSidebar.classList.remove('open');
        if (filtersOverlay) filtersOverlay.classList.remove('visible');
    }

    if (openFiltersBtn) openFiltersBtn.addEventListener('click', openFilters);
    if (closeFiltersBtn) closeFiltersBtn.addEventListener('click', closeFilters);
    if (filtersOverlay) filtersOverlay.addEventListener('click', closeFilters);

    // --- LÓGICA PARA LAS TARJETAS DE PRODUCTO ---
    const productCards = document.querySelectorAll('.product-card');
    let productoActivo = null;
    const apiBase = '/compras/api';

    const getCSRFToken = () => {
        const match = document.cookie.match(new RegExp('(^| )csrftoken=([^;]+)'));
        if (match) return decodeURIComponent(match[2]);
        return null;
    };

    async function fetchCarrito() {
        try {
            const resp = await fetch(`${apiBase}/shopcart/`, { credentials: 'include' });
            if (!resp.ok) throw new Error(await resp.text());
            const data = await resp.json();
            const items = data.items || [];
            // normalizamos a {id, cantidad}
            return items.map((it) => ({
                id: String(it.productId ?? it.producto_id ?? it.id),
                cantidad: Number(it.quantity ?? it.cantidad ?? 1),
                product: it.product || {},
            }));
        } catch (err) {
            console.error('No se pudo obtener el carrito', err);
            return [];
        }
    }

    async function actualizarCantidadAPI(productId, cantidad) {
        const csrf = getCSRFToken() || '';
        console.log('Carrito: actualizar', { productId, cantidad });
        try {
            if (cantidad <= 0) {
                // Eliminar producto del carrito
                const resp = await fetch(`${apiBase}/shopcart/${productId}/`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: { 'X-CSRFToken': csrf },
                });
                if (!resp.ok) {
                    const msg = await resp.text();
                    console.error('Carrito DELETE fallo', resp.status, msg);
                    // Si el item no existe (404), solo sincronizamos sin lanzar error
                    if (resp.status !== 404) throw new Error(msg);
                }
            } else {
                // Verificar si el producto ya existe en el carrito
                const carritoActual = await fetchCarrito();
                const existeEnCarrito = carritoActual.some(item => item.id === String(productId));

                if (existeEnCarrito) {
                    // Actualizar cantidad existente usando PUT
                    const resp = await fetch(`${apiBase}/shopcart/${productId}/`, {
                        method: 'PUT',
                        credentials: 'include',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrf,
                        },
                        body: JSON.stringify({ quantity: cantidad }),
                    });
                    if (!resp.ok) {
                        const msg = await resp.text();
                        console.error('Carrito PUT fallo', resp.status, msg);
                        throw new Error(msg);
                    }
                } else {
                    // Agregar nuevo producto usando POST
                    const resp = await fetch(`${apiBase}/shopcart/`, {
                        method: 'POST',
                        credentials: 'include',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrf,
                        },
                        body: JSON.stringify({ productId, quantity: cantidad }),
                    });
                    if (!resp.ok) {
                        const msg = await resp.text();
                        console.error('Carrito POST fallo', resp.status, msg);
                        throw new Error(msg);
                    }
                }
            }
        } catch (err) {
            console.error('Error actualizando carrito', err);
            throw err;
        }
    }

    async function syncCarritoYDisparar() {
        const carritoActual = await fetchCarrito();

        // Sincronizar con sessionStorage para el badge del navbar
        const carritoMock = carritoActual.map(item => {
            // Extraer imagen - manejar campo 'imagenes' que puede ser objeto o lista
            let imagen = 'https://via.placeholder.com/120x120';
            const imagenes = item.product?.imagenes || item.product?.imagen || item.product?.image || item.product?.image_url;

            if (imagenes) {
                if (typeof imagenes === 'string') {
                    imagen = imagenes;
                } else if (typeof imagenes === 'object' && !Array.isArray(imagenes)) {
                    imagen = imagenes.url || imagen;
                } else if (Array.isArray(imagenes) && imagenes.length > 0) {
                    const principal = imagenes.find(img => img.esPrincipal);
                    if (principal && principal.url) {
                        imagen = principal.url;
                    } else if (imagenes[0]) {
                        imagen = typeof imagenes[0] === 'string' ? imagenes[0] : (imagenes[0].url || imagen);
                    }
                }
            }

            return {
                id: item.id,
                cantidad: item.cantidad,
                nombre: item.product?.nombre || `Producto ${item.id}`,
                precio: item.product?.precio || 0,
                imagen: imagen
            };
        });
        sessionStorage.setItem('carrito_demo', JSON.stringify(carritoMock));

        // Disparar evento para actualizar vistas
        document.dispatchEvent(new CustomEvent('cartUpdated', { detail: { carrito: carritoActual } }));

        // Actualizar manualmente el badge del carrito
        if (window.actualizarVistaCarrito) {
            window.actualizarVistaCarrito();
        }
    }

    function confirmarProductoActivo() {
        if (productoActivo === null) return;
        const cardActiva = document.querySelector(`.product-card[data-id="${productoActivo}"]`);
        if (cardActiva) {
            const quantityInput = cardActiva.querySelector('.quantity-input');
            const cantidad = parseInt(quantityInput.value) || 0;
            const idConfirmado = productoActivo;

            // Limpiamos el estado ANTES de actualizar, para que la tarjeta se pueda redibujar.
            productoActivo = null;

            // Actualizamos el carrito. Esto disparará 'cartUpdated' para todas las tarjetas.
            window.actualizarCantidadProducto(idConfirmado, cantidad);
        } else {
            productoActivo = null;
        }
    }

    const actualizarVistaTarjeta = (card, carrito) => {
        const productId = card.dataset.id;
        const actionsContainer = card.querySelector('.card-actions');
        const addToCartBtn = actionsContainer.querySelector('.add-to-cart-btn');
        const quantitySelector = actionsContainer.querySelector('.quantity-selector');
        const confirmBtn = actionsContainer.querySelector('.confirm-btn');
        const quantityInput = actionsContainer.querySelector('.quantity-input');

        // Si la tarjeta está en modo edición, no la actualizamos desde aquí.
        if (productId === productoActivo) return;

        const productoEnCarrito = carrito.find(item => item.id === productId);
        if (productoEnCarrito) {
            // Estado normal: en el carrito (solo se ve el selector)
            addToCartBtn.classList.add('hidden');
            confirmBtn.classList.add('hidden');
            quantitySelector.classList.remove('hidden');
            quantityInput.value = productoEnCarrito.cantidad;
        } else {
            // Estado normal: no en el carrito (solo se ve "Agregar")
            addToCartBtn.classList.remove('hidden');
            confirmBtn.classList.add('hidden');
            quantitySelector.classList.add('hidden');
            quantityInput.value = 1;
        }
    };

    productCards.forEach(card => {
        const productId = card.dataset.id;
        const actionsContainer = card.querySelector('.card-actions');
        const addToCartBtn = actionsContainer.querySelector('.add-to-cart-btn');
        const confirmBtn = actionsContainer.querySelector('.confirm-btn');
        const plusBtn = actionsContainer.querySelector('.plus-btn');
        const minusBtn = actionsContainer.querySelector('.minus-btn');
        const quantityInput = actionsContainer.querySelector('.quantity-input');
        const quantitySelector = actionsContainer.querySelector('.quantity-selector');
        const removeBtn = actionsContainer.querySelector('.remove-btn');

        function entrarModoEdicion() {
            if (productoActivo !== null && productoActivo !== productId) {
                confirmarProductoActivo();
            }
            productoActivo = productId;

            // Vista de "modo edición"
            addToCartBtn.classList.add('hidden');
            quantitySelector.classList.remove('hidden');
            confirmBtn.classList.remove('hidden');
        }

        addToCartBtn.addEventListener('click', async () => {
            try {
                await window.actualizarCantidadProducto(productId, 1);
            } catch (e) {
                alert('No se pudo agregar el producto al carrito. Revisa tu sesion.');
            }
        });
        quantitySelector.addEventListener('click', (e) => {
            if (e.target.classList.contains('quantity-btn')) entrarModoEdicion();
        });

        quantityInput.addEventListener('input', () => {
            // 1. Filtra el valor para permitir solo números
            quantityInput.value = quantityInput.value.replace(/[^0-9]/g, '');
            // 2. Activa el modo edición para mostrar "Confirmar"
            entrarModoEdicion();
        });

        plusBtn.addEventListener('click', () => {
            quantityInput.value = (parseInt(quantityInput.value) || 0) + 1;
        });

        minusBtn.addEventListener('click', () => {
            const currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
            }
        });

        confirmBtn.addEventListener('click', confirmarProductoActivo);

        if (removeBtn) {
            removeBtn.addEventListener('click', async () => {
                try {
                    await window.actualizarCantidadProducto(productId, 0);
                } catch (e) {
                    alert('No se pudo eliminar el producto del carrito.');
                }
            });
        }
    });

    document.addEventListener('cartUpdated', (e) => {
        const carritoActual = e.detail.carrito;
        productCards.forEach(card => {
            actualizarVistaTarjeta(card, carritoActual);
        });
    });

    // Expone función global usada por las tarjetas
    window.actualizarCantidadProducto = async (productId, cantidad) => {
        try {
            await actualizarCantidadAPI(productId, cantidad);
            await syncCarritoYDisparar();
        } catch (err) {
            alert('No se pudo actualizar el carrito. Revisa tu sesión o intenta de nuevo.');
        }
    };

    // Cargar carrito real y pintar vistas
    (async () => {
        const carrito = await fetchCarrito();

        // Sincronizar con sessionStorage para el badge del navbar
        const carritoMock = carrito.map(item => {
            // Extraer imagen - manejar campo 'imagenes' que puede ser objeto o lista
            let imagen = 'https://via.placeholder.com/120x120';
            const imagenes = item.product?.imagenes || item.product?.imagen || item.product?.image || item.product?.image_url;

            if (imagenes) {
                if (typeof imagenes === 'string') {
                    imagen = imagenes;
                } else if (typeof imagenes === 'object' && !Array.isArray(imagenes)) {
                    imagen = imagenes.url || imagen;
                } else if (Array.isArray(imagenes) && imagenes.length > 0) {
                    const principal = imagenes.find(img => img.esPrincipal);
                    if (principal && principal.url) {
                        imagen = principal.url;
                    } else if (imagenes[0]) {
                        imagen = typeof imagenes[0] === 'string' ? imagenes[0] : (imagenes[0].url || imagen);
                    }
                }
            }

            return {
                id: item.id,
                cantidad: item.cantidad,
                nombre: item.product?.nombre || `Producto ${item.id}`,
                precio: item.product?.precio || 0,
                imagen: imagen
            };
        });
        sessionStorage.setItem('carrito_demo', JSON.stringify(carritoMock));

        productCards.forEach(card => {
            actualizarVistaTarjeta(card, carrito);
        });
        document.dispatchEvent(new CustomEvent('cartUpdated', { detail: { carrito } }));

        // Actualizar el badge del carrito
        if (window.actualizarVistaCarrito) {
            window.actualizarVistaCarrito();
        }
    })();
});
