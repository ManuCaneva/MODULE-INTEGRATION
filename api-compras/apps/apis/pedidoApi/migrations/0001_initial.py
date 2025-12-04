from __future__ import annotations

import decimal

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DireccionEnvio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_receptor', models.CharField(max_length=255)),
                ('calle', models.CharField(max_length=255)),
                ('ciudad', models.CharField(max_length=120)),
                ('provincia', models.CharField(blank=True, max_length=120)),
                ('codigo_postal', models.CharField(max_length=20)),
                ('pais', models.CharField(default='Argentina', max_length=120)),
                ('telefono', models.CharField(blank=True, max_length=30)),
                ('informacion_adicional', models.CharField(blank=True, max_length=255)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='direcciones_envio', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-creado_en'],
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('borrador', 'Borrador'), ('pendiente', 'Pendiente'), ('confirmado', 'Confirmado'), ('cancelado', 'Cancelado')], default='pendiente', max_length=20)),
                ('tipo_transporte', models.CharField(blank=True, max_length=50)),
                ('total', models.DecimalField(decimal_places=2, default=decimal.Decimal('0.00'), max_digits=12, validators=[django.core.validators.MinValueValidator(decimal.Decimal('0.00'))])),
                ('referencia_envio', models.CharField(blank=True, max_length=120)),
                ('referencia_reserva_stock', models.CharField(blank=True, max_length=120)),
                ('confirmado_en', models.DateTimeField(blank=True, null=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('direccion_envio', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='pedido', to='pedidoApi.direccionenvio')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pedidos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-creado_en'],
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto_id', models.PositiveIntegerField()),
                ('nombre_producto', models.CharField(max_length=255)),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(decimal.Decimal('0.00'))])),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='pedidoApi.pedido')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
