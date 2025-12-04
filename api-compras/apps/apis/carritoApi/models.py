from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Carrito(models.Model):
	usuario = models.ForeignKey(User,blank=True, null=True ,on_delete=models.CASCADE, related_name='carritos')
	creado_en = models.DateTimeField(auto_now_add=True)
	actualizado_en = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Carrito de {self.usuario}"  

class ItemCarrito(models.Model):
	carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
	producto_id = models.IntegerField()
	cantidad = models.PositiveIntegerField(default=1)
	agregado_en = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Producto {self.producto_id} x{self.cantidad}"


# Create your models here.

# fran no muestra esto!

