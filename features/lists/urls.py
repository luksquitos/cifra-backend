from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from features.lists import viewsets

router = SimpleRouter()
router.register("", viewsets.ListViewSet, "Lists")

product_list_router = NestedSimpleRouter(router, "", lookup="list")
product_list_router.register("products", viewsets.ProductListViewSet, "ProductList")


urlpatterns = [
    path("", include(product_list_router.urls)),
    path("", include(router.urls)),
]
