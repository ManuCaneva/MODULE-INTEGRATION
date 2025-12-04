from rest_framework.routers import DefaultRouter
from .views import CartViewSet

router = DefaultRouter()
router.register(r'shopcart', CartViewSet, basename='shopcart')

urlpatterns = router.urls
