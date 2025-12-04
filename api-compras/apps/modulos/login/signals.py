# login/signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import re

User = get_user_model()

@receiver(pre_save, sender=User)
def ensure_unique_username(sender, instance, **kwargs):
    """
    Genera un username único basado en el correo electrónico del usuario
    antes de que se guarde en la base de datos.
    """
    if not instance.username:
        # Generar la base del username a partir del correo electrónico
        base_username = instance.email.split('@')[0].lower()
        # Eliminar caracteres no alfanuméricos
        base_username = re.sub(r'\W+', '', base_username)
        username = base_username
        counter = 1
        # Verificar la unicidad del username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        instance.username = username