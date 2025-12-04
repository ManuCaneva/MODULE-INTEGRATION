"""
NOTA: Este módulo ahora usa los modelos de pedidoApi.
Los modelos locales están comentados para evitar conflictos.
"""

# Importar modelos desde la API (fuente única de verdad)
from apps.apis.pedidoApi.models import Pedido, DetallePedido, DireccionEnvio

# Modelos originales (desactivados - solo para referencia/simulación)
"""
from django.db import models
from django.conf import settings

class Pedido(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos_modulo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f'Pedido #{self.pk} - {self.user.username}'

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto_nombre = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} x {self.producto_nombre}'

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
"""
