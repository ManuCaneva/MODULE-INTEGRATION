from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from .models import DetallePedido, DireccionEnvio, Pedido


class DireccionEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DireccionEnvio
        fields = [
            "id",
            "nombre_receptor",
            "calle",
            "ciudad",
            "provincia",
            "codigo_postal",
            "pais",
            "telefono",
            "informacion_adicional",
        ]
        read_only_fields = ["id"]


class DetallePedidoSerializer(serializers.ModelSerializer):
    precio_total = serializers.SerializerMethodField()

    class Meta:
        model = DetallePedido
        fields = [
            "id",
            "producto_id",
            "nombre_producto",
            "cantidad",
            "precio_unitario",
            "precio_total",
        ]
        read_only_fields = ["id", "precio_total"]

    def get_precio_total(self, detalle: DetallePedido) -> Decimal:
        return detalle.precio_total


class PedidoSerializer(serializers.ModelSerializer):
    direccion_envio = DireccionEnvioSerializer(required=False)
    detalles = DetallePedidoSerializer(many=True, required=False)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Pedido
        fields = [
            "id",
            "usuario",
            "estado",
            "estado_display",
            "tipo_transporte",
            "total",
            "referencia_envio",
            "referencia_reserva_stock",
            "confirmado_en",
            "creado_en",
            "actualizado_en",
            "direccion_envio",
            "detalles",
        ]
        read_only_fields = [
            "id",
            "usuario",
            "estado",
            "estado_display",
            "total",
            "referencia_envio",
            "referencia_reserva_stock",
            "confirmado_en",
            "creado_en",
            "actualizado_en",
        ]

    def _obtener_usuario(self):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return request.user
        return None

    @transaction.atomic
    def create(self, datos_validados):
        datos_detalles = datos_validados.pop("detalles", None)
        datos_direccion = datos_validados.pop("direccion_envio", None)

        if not datos_detalles:
            raise serializers.ValidationError({"detalles": "Debe indicar los productos del pedido."})
        if not datos_direccion:
            raise serializers.ValidationError({"direccion_envio": "Debe indicar la dirección de envío."})

        usuario = self._obtener_usuario()
        direccion = DireccionEnvio.objects.create(usuario=usuario, **datos_direccion)
        tipo_transporte = datos_validados.pop("tipo_transporte", "")
        pedido = Pedido.objects.create(
            usuario=usuario,
            direccion_envio=direccion,
            tipo_transporte=tipo_transporte,
        )

        total = Decimal("0.00")
        for datos_detalle in datos_detalles:
            detalle = DetallePedido.objects.create(pedido=pedido, **datos_detalle)
            total += detalle.precio_total

        pedido.total = total
        pedido.save(update_fields=["total", "actualizado_en"])
        return pedido

    @transaction.atomic
    def update(self, instancia: Pedido, datos_validados):
        if instancia.estado == Pedido.Estado.CONFIRMADO:
            raise serializers.ValidationError("No se puede modificar un pedido confirmado.")

        datos_detalles = datos_validados.pop("detalles", None)
        datos_direccion = datos_validados.pop("direccion_envio", None)

        campos_a_actualizar: list[str] = []
        tipo_transporte = datos_validados.get("tipo_transporte")
        if tipo_transporte is not None:
            instancia.tipo_transporte = tipo_transporte
            campos_a_actualizar.append("tipo_transporte")

        if campos_a_actualizar:
            campos_a_actualizar.append("actualizado_en")
            instancia.save(update_fields=campos_a_actualizar)

        if datos_direccion:
            for atributo, valor in datos_direccion.items():
                setattr(instancia.direccion_envio, atributo, valor)
            instancia.direccion_envio.save()
            instancia.save(update_fields=["actualizado_en"])

        if datos_detalles is not None:
            instancia.detalles.all().delete()
            total = Decimal("0.00")
            for datos_detalle in datos_detalles:
                detalle = DetallePedido.objects.create(pedido=instancia, **datos_detalle)
                total += detalle.precio_total
            instancia.total = total
            instancia.save(update_fields=["total", "actualizado_en"])

        return instancia

    def to_representation(self, instancia):
        representacion = super().to_representation(instancia)

        # Asegurar que se incluyan los detalles
        representacion["detalles"] = DetallePedidoSerializer(
            instancia.detalles.all(),
            many=True
        ).data

        # Asegurar que se incluya la dirección de envío
        if instancia.direccion_envio:
            representacion["direccion_envio"] = DireccionEnvioSerializer(
                instancia.direccion_envio
            ).data

        # Formatear total como string
        representacion["total"] = str(instancia.total)

        return representacion
