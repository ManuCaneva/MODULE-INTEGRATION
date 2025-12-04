from django.contrib.auth.backends import BaseBackend
from apps.administracion.models import Usuario

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = Usuario.objects.get(email=email)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None