from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class DireccionEnvio(models.Model):
    """Dirección de envío asociada a un pedido."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="direcciones_envio",
        null=True,
        blank=True,
    )
    nombre_receptor = models.CharField(max_length=255)
    calle = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=120)
    provincia = models.CharField(max_length=120, blank=True)
    codigo_postal = models.CharField(max_length=20)
    pais = models.CharField(max_length=120, default="Argentina")
    telefono = models.CharField(max_length=30, blank=True)
    informacion_adicional = models.CharField(max_length=255, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return f"{self.nombre_receptor} - {self.calle}, {self.ciudad}"

    def generar_datos_logistica(self) -> dict[str, str]:
        """Devuelve el payload esperado por el servicio de logística."""
        state = (self.provincia or self.ciudad or "").strip()
        cp = (self.codigo_postal or "").strip()
        payload = {
            "street": self.calle,
            "city": self.ciudad,
            "state": state,
            "postal_code": cp,
            "country": self.pais,
        }
        return payload


class Pedido(models.Model):
    """Pedido del usuario que agrupa ítems y dirección de envío."""

    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADO = "confirmado", "Confirmado"
        CANCELADO = "cancelado", "Cancelado"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="pedidos",
        null=True,
        blank=True,
    )
    direccion_envio = models.OneToOneField(
        DireccionEnvio,
        on_delete=models.PROTECT,
        related_name="pedido",
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    tipo_transporte = models.CharField(max_length=50, blank=True)
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    referencia_envio = models.CharField(max_length=120, blank=True)
    referencia_reserva_stock = models.CharField(max_length=120, blank=True)
    confirmado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return f"Pedido #{self.pk} ({self.get_estado_display()})"

    def recalcular_total(self, guardar: bool = True) -> Decimal:
        total_calculado = sum((detalle.precio_total for detalle in self.detalles.all()), Decimal("0.00"))
        self.total = total_calculado
        if guardar:
            self.save(update_fields=["total", "actualizado_en"])
        return total_calculado

    def marcar_confirmado(
        self,
        *,
        referencia_envio: str,
        referencia_reserva_stock: str,
    ) -> None:
        self.estado = self.Estado.CONFIRMADO
        self.referencia_envio = referencia_envio
        self.referencia_reserva_stock = referencia_reserva_stock
        self.confirmado_en = timezone.now()
        self.save(
            update_fields=[
                "estado",
                "referencia_envio",
                "referencia_reserva_stock",
                "confirmado_en",
                "actualizado_en",
            ]
        )


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    producto_id = models.PositiveIntegerField()
    nombre_producto = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:  # pragma: no cover - representación simple
        return f"{self.nombre_producto} x{self.cantidad}"

    @property
    def precio_total(self) -> Decimal:
        return self.precio_unitario * self.cantidad
