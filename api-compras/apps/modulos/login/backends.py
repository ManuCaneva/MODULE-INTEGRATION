from django.contrib.auth.backends import ModelBackend
from apps.administracion.models import Usuario

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return None

        if usuario.check_password(password):
            return usuario