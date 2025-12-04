document.addEventListener('DOMContentLoaded', function () {
    lottie.loadAnimation({
        container: document.getElementById('lottie-animation-failure'),
        renderer: 'svg',
        loop: false,
        autoplay: true,
        path: "/compras/static/lottie/apps/modulos/pedidos/failed.json" 
    });
});