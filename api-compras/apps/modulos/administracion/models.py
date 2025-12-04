from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission



class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    vac = models.BooleanField(default=False)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"username='{self.username}', "
            f"email='{self.email}', "
            f"telefono='{self.telefono}', "
            f"direccion='{self.direccion}', "
            f"vac={self.vac}, "
            f"fecha_nacimiento={self.fecha_nacimiento}, "
            f"fecha_registro={self.fecha_registro}"
        )

    class Meta:
        db_table = "usuario"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
