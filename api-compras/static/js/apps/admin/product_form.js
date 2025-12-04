
document.addEventListener('DOMContentLoaded', function() {
    const tipoSelector = document.getElementById('clase_producto');
    const indumentariaFields = document.getElementById('indumentaria_fields');
    const metodoPrecio = document.getElementById('metodo_precio');
    const costoInput = document.getElementById('costo');
    const porcentajeInput = document.getElementById('porcentaje');
    const extraInput = document.getElementById('valor_extra');
    const precioFinalInput = document.getElementById('precio');

    function actualizarPrecio() {
        const costo = parseFloat(costoInput.value) || 0;
        const porcentaje = parseFloat(porcentajeInput.value) || 0;
        const extra = parseFloat(extraInput.value) || 0;
        let final = costo;
        if (metodoPrecio.value === 'costo_porcentaje') {
            final = costo + costo * porcentaje / 100;
        } else if (metodoPrecio.value === 'costo_valor') {
            final = costo + extra;
        } else if (metodoPrecio.value === 'valor_directo') {
            final = extra;
        }
        precioFinalInput.value = final.toFixed(2);
    }

    function actualizarTipo() {
        indumentariaFields.style.display = 'none';
        if (tipoSelector.value === 'indumentaria') {
            indumentariaFields.style.display = 'block';
        }
    }

    tipoSelector.addEventListener('change', actualizarTipo);
    metodoPrecio.addEventListener('change', actualizarPrecio);
    costoInput.addEventListener('input', actualizarPrecio);
    porcentajeInput.addEventListener('input', actualizarPrecio);
    extraInput.addEventListener('input', actualizarPrecio);

    actualizarTipo();
    actualizarPrecio();
});

