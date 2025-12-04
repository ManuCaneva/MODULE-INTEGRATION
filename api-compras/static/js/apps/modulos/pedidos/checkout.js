document.addEventListener('DOMContentLoaded', () => {
    let currentStep = 1;
    const steps = document.querySelectorAll('.checkout-step');
    const stepIndicators = document.querySelectorAll('.stepper .step');
    const orderStatusCard = document.getElementById('order-status-card');
    const summaryItemsContainer = document.querySelector('.summary-items');
    const totalsSummaryContainer = document.querySelector('.totals-summary');
    const shippingDetailsSection = document.getElementById('shipping-details');
    const shippingRadios = document.querySelectorAll('input[name="tipo_envio"]');

    const config = window.checkoutConfig || {};
    const apiBase = (config.apiBase || '').replace(/\/$/, '');
    const checkoutUrl = config.checkoutUrl || `${apiBase}/shopcart/checkout`;
    const successUrl = config.successUrl || '/pedidos/pago/exitoso/';
    const failureUrl = config.failureUrl || '';

    let carritoItems = [];
    let shippingQuote = null;

    const joinUrl = (base, path) => {
        if (!base) return path;
        if (path.startsWith('http')) return path;
        const normalizedBase = base.endsWith('/') ? base.slice(0, -1) : base;
        const normalizedPath = path.startsWith('/') ? path : `/${path}`;
        return `${normalizedBase}${normalizedPath}`;
    };

    const getCSRFToken = () => {
        const match = document.cookie.match(new RegExp('(^| )csrftoken=([^;]+)'));
        if (match) return decodeURIComponent(match[2]);
        return null;
    };

    const formatPrice = (value) => `$ ${Number(value || 0).toLocaleString('es-AR')}`;

    const renderSummaryItems = () => {
        if (!summaryItemsContainer) return;

        summaryItemsContainer.innerHTML = '';
        let subtotal = 0;

        if (!carritoItems.length) {
            summaryItemsContainer.innerHTML = '<p class="cart-empty-summary">No hay productos en el carrito.</p>';
        } else {
            carritoItems.forEach((item) => {
                const product = item.product || {};
                const price = parseFloat(
                    product.price ??
                    product.precio ??
                    product.precio_unitario ??
                    0
                ) || 0;
                const qty = item.quantity ?? item.cantidad ?? 1;
                const name = product.name || product.nombre || `Producto ${item.productId || item.producto_id || ''}`;
                
                // Extraer imagen - manejar campo 'imagenes' que puede ser objeto o lista
                let image = 'https://via.placeholder.com/120x120/f1f1f1/cccccc?text=Producto';
                const imagenes = product.imagenes || product.imagen || product.image || product.image_url;

                if (imagenes) {
                    if (typeof imagenes === 'string') {
                        // Si es string directo, usarlo
                        image = imagenes;
                    } else if (typeof imagenes === 'object' && !Array.isArray(imagenes)) {
                        // Si es un objeto, buscar la URL
                        image = imagenes.url || image;
                    } else if (Array.isArray(imagenes) && imagenes.length > 0) {
                        // Si es una lista, buscar la imagen principal o la primera
                        const principal = imagenes.find(img => img.esPrincipal);
                        if (principal && principal.url) {
                            image = principal.url;
                        } else if (imagenes[0]) {
                            image = typeof imagenes[0] === 'string' ? imagenes[0] : (imagenes[0].url || image);
                        }
                    }
                }
                
                const itemSubtotal = price * qty;
                subtotal += itemSubtotal;

                const div = document.createElement('div');
                div.className = 'summary-item';
                div.innerHTML = `
                    <img src="${image}" alt="${name}" class="item-image">
                    <div class="item-details">
                        <p>${name}</p>
                        <span>${qty > 1 ? 'x' + qty : ''}</span>
                    </div>
                    <span class="item-price">${formatPrice(itemSubtotal)}</span>
                `;
                summaryItemsContainer.appendChild(div);
            });
        }

        if (totalsSummaryContainer) {
            const rows = totalsSummaryContainer.querySelectorAll('.total-row span:last-child');
            const envio = shippingQuote == null ? '-' : formatPrice(shippingQuote);
            const shippingValue = shippingQuote == null ? 0 : shippingQuote;

            if (rows && rows.length >= 3) {
                rows[0].textContent = formatPrice(subtotal);
                rows[1].textContent = envio;
                rows[2].textContent = formatPrice(subtotal + shippingValue);
            }
        }
    };

    // Mapeo de tipos de transporte a nombres legibles
    const transportTypeNames = {
        'air': 'Air Transport',
        'sea': 'Sea Transport',
        'road': 'Road Transport',
        'rail': 'Rail Transport',
        'domicilio': 'Envío a domicilio',
        'demo_tracking': 'Demo con seguimiento',
    };

    const getTransportName = (value) => {
        return transportTypeNames[value] || value;
    };

    const populateFinalSummary = () => {
        const nombre = document.getElementById('nombre')?.value || '';
        const telefono = document.getElementById('telefono')?.value || '';
        const calle = document.getElementById('calle')?.value || '';
        const depto = document.getElementById('departamento')?.value || '';
        const ciudad = document.getElementById('ciudad')?.value || '';
        const provincia = document.getElementById('provincia')?.value || '';
        const cp = document.getElementById('codigo_postal')?.value || '';

        const shippingRadio = document.querySelector('input[name="tipo_envio"]:checked');
        const shippingSection = document.getElementById('summary-shipping-section');

        const summaryNombre = document.getElementById('summary-nombre');
        const summaryTelefono = document.getElementById('summary-telefono');
        if (summaryNombre) summaryNombre.textContent = nombre || 'No especificado';
        if (summaryTelefono) summaryTelefono.textContent = telefono || 'No especificado';

        if (shippingRadio) {
            const transportType = shippingRadio.value;
            const shippingMethod = document.getElementById('summary-shipping-method');
            
            if (transportType === 'domicilio') {
                if (shippingSection) shippingSection.style.display = 'block';

                let addressLine1 = calle;
                if (depto) addressLine1 += `, ${depto}`;

                const line1 = document.getElementById('summary-address-line1');
                const line2 = document.getElementById('summary-address-line2');
                if (line1) line1.textContent = addressLine1;
                if (line2) line2.textContent = `${ciudad}${provincia ? ', ' + provincia : ''}${cp ? ' (' + cp + ')' : ''}`;

                if (shippingMethod) shippingMethod.textContent = 'Envío a domicilio';
                orderStatusCard?.classList.add('hidden');
            } else if (transportType === 'demo_tracking') {
                if (shippingSection) shippingSection.style.display = 'none';
                if (shippingMethod) shippingMethod.textContent = 'Demo con seguimiento';
                if (orderStatusCard) {
                    orderStatusCard.classList.remove('hidden');
                    orderStatusCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            } else {
                // Para tipos de transporte (air, sea, road, rail)
                if (shippingSection) shippingSection.style.display = 'none';
                if (shippingMethod) shippingMethod.textContent = getTransportName(transportType);
                orderStatusCard?.classList.add('hidden');
            }
        }
    };

    const updateStepUI = () => {
        steps.forEach((step, index) => {
            const stepNumber = index + 1;
            step.classList.toggle('hidden', stepNumber !== currentStep);
        });

        stepIndicators.forEach((indicator, index) => {
            const stepNumber = index + 1;
            indicator.classList.remove('active', 'completed');

            const nextConnector = indicator.nextElementSibling;
            let progressLine = null;
            if (nextConnector && nextConnector.classList.contains('step-connector')) {
                progressLine = nextConnector.querySelector('.connector-line-progress');
            }

            if (stepNumber < currentStep) {
                indicator.classList.add('completed');
                if (progressLine) {
                    progressLine.style.width = '100%';
                    progressLine.style.backgroundColor = 'var(--color-green)';
                }
            } else if (stepNumber === currentStep) {
                indicator.classList.add('active');
                if (progressLine) {
                    setTimeout(() => {
                        progressLine.style.width = '50%';
                        progressLine.style.backgroundColor = 'var(--color-active)';
                    }, 50);
                }
            } else if (progressLine) {
                progressLine.style.width = '0%';
            }
        });

        if (currentStep === 3) {
            populateFinalSummary();
        }
    };

    const toggleShippingDetails = () => {
        const selected = document.querySelector('input[name="tipo_envio"]:checked');
        if (selected && selected.value !== 'retiro_sucursal') {
            if (shippingDetailsSection) shippingDetailsSection.style.display = 'block';
        } else if (shippingDetailsSection) {
            shippingDetailsSection.style.display = 'none';
        }
    };

    const loadCart = async () => {
        try {
            const resp = await fetch(joinUrl(apiBase, '/shopcart/'), {
                credentials: 'include',
            });
            if (resp.status === 401) {
                console.warn('Checkout loadCart 401 - sesion requerida');
                if (summaryItemsContainer) {
                    summaryItemsContainer.innerHTML = '<p class="cart-empty-summary">Inicia sesion para ver tu carrito.</p>';
                }
                return;
            }
            if (!resp.ok) {
                console.error('Checkout loadCart fallo', resp.status);
                throw new Error(await resp.text());
            }
            const data = await resp.json();
            carritoItems = data.items || [];
            console.log('Checkout loadCart items', carritoItems);
            renderSummaryItems();
        } catch (err) {
            console.error('Error al obtener el carrito', err);
            if (summaryItemsContainer) {
                summaryItemsContainer.innerHTML = '<p class="cart-empty-summary">No se pudo cargar el carrito.</p>';
            }
        }
    };

    shippingRadios.forEach((radio) =>
        radio.addEventListener('change', () => {
            shippingQuote = null;
            toggleShippingDetails();
            renderSummaryItems();
        })
    );

    document.querySelectorAll('.btn-next').forEach((button) => {
        button.addEventListener('click', () => {
            if (currentStep < steps.length) {
                currentStep++;
                updateStepUI();
            }
        });
    });

    document.querySelectorAll('.btn-prev').forEach((button) => {
        button.addEventListener('click', () => {
            if (currentStep > 1) {
                currentStep--;
                updateStepUI();
            }
        });
    });

    document.querySelectorAll('.btn-secondary').forEach((button) => {
        button.addEventListener('click', () => {
            window.location.href = '/';
        });
    });

    const mostrarResultado = (data, status) => {
        if (!orderStatusCard) return;
        orderStatusCard.classList.remove('hidden');
        orderStatusCard.innerHTML = '';

        if (status >= 200 && status < 300) {
            const pedido = data.pedido || {};
            const reserva = data.reserva || {};
            const envio = data.envio || {};
            orderStatusCard.innerHTML = `
                <h3>Pedido confirmado</h3>
                <p><strong>Pedido ID:</strong> ${pedido.id || data.pedido_id || '-'}</p>
                <p><strong>Estado:</strong> ${pedido.estado || '-'}</p>
                <p><strong>Reserva stock:</strong> ${reserva.id || reserva.reservationId || JSON.stringify(reserva)}</p>
                <p><strong>Envio / Tracking:</strong> ${envio.id || envio.shipping_id || envio.trackingId || JSON.stringify(envio)}</p>
            `;
        } else {
            orderStatusCard.innerHTML = `
                <h3>Error procesando pedido</h3>
                <p>${data && data.error ? data.error : 'Ocurrio un error al procesar el pedido.'}</p>
                <pre style="white-space:pre-wrap">${data && data.detail ? JSON.stringify(data.detail) : ''}</pre>
            `;
        }
        orderStatusCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    const finalizarPedido = async (event) => {
        event.preventDefault();
        const btn = event?.currentTarget;
        if (btn) btn.disabled = true;

        const nombre = document.getElementById('nombre')?.value || '';
        const telefono = document.getElementById('telefono')?.value || '';
        const calle = document.getElementById('calle')?.value || '';
        const departamento = document.getElementById('departamento')?.value || '';
        const ciudad = document.getElementById('ciudad')?.value || '';
        const codigo_postal = document.getElementById('codigo_postal')?.value || '';
        const provincia = document.getElementById('provincia')?.value || '';
        const info_adicional = document.getElementById('informacion_adicional')?.value || '';
        const tipo_envio_el = document.querySelector('input[name="tipo_envio"]:checked');
        const tipo_transporte = tipo_envio_el?.value || 'domicilio';
        const metodo_pago = document.getElementById('payment_method')?.value || 'tarjeta';

        const items_payload = carritoItems
            .map((it) => {
                const pid = it.productId || it.producto_id || it.id;
                const qty = it.quantity || it.cantidad || 1;
                return pid ? { productId: Number(pid), quantity: Number(qty) } : null;
            })
            .filter(Boolean);

        console.log('Checkout enviar payload items', items_payload);

        if (!items_payload.length) {
            alert('El carrito esta vacio.');
            if (btn) btn.disabled = false;
            return;
        }

        if (!nombre || !telefono) {
            alert('Por favor completa nombre y telefono.');
            if (btn) btn.disabled = false;
            return;
        }

        if (tipo_transporte !== 'retiro_sucursal' && tipo_transporte !== 'demo_tracking') {
            const postalRegex = /^[A-Za-z]\d{4}[A-Za-z]{3}$/;
            if (!calle || !ciudad || !codigo_postal || !provincia) {
                alert('Por favor completa calle, ciudad, provincia y codigo postal.');
                if (btn) btn.disabled = false;
                return;
            }
            if (!postalRegex.test(codigo_postal.trim())) {
                alert('El codigo postal debe tener formato A1234ABC (una letra, 4 numeros y 3 letras).');
                if (btn) btn.disabled = false;
                return;
            }
        }

        const payload = {
            direccion_envio: {
                nombre_receptor: nombre,
                telefono: telefono,
                calle: calle,
                ciudad: ciudad,
                codigo_postal: codigo_postal,
                provincia: provincia,
                pais: 'Argentina',
                informacion_adicional: info_adicional || departamento,
            },
            tipo_transporte: tipo_transporte,
            metodo_pago: metodo_pago,
            items: items_payload,
        };

        console.group('Checkout payload');
        console.log('Endpoint', checkoutUrl);
        console.log('Direccion envio', payload.direccion_envio);
        console.log('Tipo transporte', payload.tipo_transporte);
        console.log('Items', payload.items);
        console.groupEnd();

        try {
            const resp = await fetch(checkoutUrl, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken() || '',
                },
                body: JSON.stringify(payload),
            });

            const data = await resp.json().catch(() => ({}));
            console.log('Checkout response status', resp.status, 'body', data);
            if (!resp.ok) {
                const msg = data?.error || data?.detail || 'Error al crear el pedido.';
                mostrarResultado(data, resp.status);
                alert(msg);
                if (failureUrl) {
                    window.location.href = failureUrl;
                }
                return;
            }

            const costo = data?.envio?.total_cost ?? data?.envio?.cost ?? null;
            if (costo !== null && !Number.isNaN(Number(costo))) {
                shippingQuote = Number(costo);
                renderSummaryItems();
            }

            mostrarResultado(data, resp.status);

            const pedidoId = data.pedido_id || data?.pedido?.id;
            if (successUrl) {
                const separator = successUrl.includes('?') ? '&' : '?';
                const redirectUrl = pedidoId ? `${successUrl}${separator}pedido=${pedidoId}` : successUrl;
                window.location.href = redirectUrl;
            } else {
                window.location.href = '/pedidos/';
            }
        } catch (error) {
            console.error('Error de red:', error);
            alert('Error de conexion al crear el pedido.');
            if (failureUrl) {
                window.location.href = failureUrl;
            }
        } finally {
            if (btn) btn.disabled = false;
        }
    };

    const confirmBtn = document.getElementById('confirm-order') || document.querySelector('.btn-confirm');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', finalizarPedido);
    }

    const checkoutForm = document.querySelector('.checkout-card form') || document.querySelector('form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', finalizarPedido);
    }

    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.addEventListener('click', finalizarPedido);
    }

    document.addEventListener('cartUpdated', () => {
        loadCart();
    });

    updateStepUI();
    toggleShippingDetails();
    loadCart();
    renderSummaryItems();
});
