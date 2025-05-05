from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from features.stores import viewsets

router = SimpleRouter()
router.register("products", viewsets.ProductViewSet, "Product")
router.register("categories", viewsets.CategoryViewSet, "Category")

historic_router = NestedSimpleRouter(router, "products", lookup="product")
historic_router.register(
    "historic", viewsets.ProductHistoricViewSet, "ProductHistoricPrice"
)

urlpatterns = [path("", include(historic_router.urls)), path("", include(router.urls))]
