from django.urls import path, include
from rest_framework.routers import SimpleRouter
from features.stores import viewsets


router = SimpleRouter()
router.register("products", viewsets.ProductViewSet, "Product")
router.register("categories", viewsets.CategoryViewSet, "Category")


urlpatterns = [
    path("", include(router.urls))
]
