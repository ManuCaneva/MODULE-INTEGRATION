"""
URL configuration for Main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.shortcuts import render
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #rutas de las apps
    #path('', include('apps.peliculas.urls')),
    path('', include('apps.modulos.inicio.urls')),
    path('administracion/', include('apps.modulos.administracion.urls')),
    path('', include('apps.modulos.login.urls')),
    path('accounts/', include('allauth.urls')),  # allauth

    path("login/", include("apps.modulos.login.urls")),
     path('pedidos/', include('apps.modulos.pedidos.urls')),
    # APIs internas (prefijo v1/)
    path('api/', include('apps.apis.carritoApi.urls')),
    path('api/', include('apps.apis.productoApi.urls')),
    path('api/', include('apps.apis.pedidoApi.urls')),
    
    # APIs del frontend (según OpenAPI) - mapean a los ViewSets correspondientes
    path('api/', include('apps.apis.pedidoApi.frontend_urls')),
    

    # Documentación Swagger/OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)