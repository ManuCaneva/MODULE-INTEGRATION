from rest_framework import serializers
from .models import  Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Categoria"""
    
    class Meta:
        model = Categoria
        fields = '__all__'  # Incluye todos los campos automáticamente
        read_only_fields = ['id', 'fecha_creacion']
