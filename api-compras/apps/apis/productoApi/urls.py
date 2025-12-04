from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

router = DefaultRouter()
router.register(r'product', ProductoViewSet, basename='producto')

urlpatterns = router.urls


