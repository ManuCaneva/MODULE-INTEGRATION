from django.urls import path
from apps.modulos.inicio import views

urlpatterns = [
   # path('QR/', views.AnalisisQR, name='AnalizarQR'),

    path('', views.inicio_view, name='inicio'),
    
]
