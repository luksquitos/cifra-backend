from rest_framework.routers import SimpleRouter
from features.products import viewsets
from django.urls import path, include


router = SimpleRouter()

router.register("",viewsets.ProductsViewSet, basename="Products")

urlpatterns = [
    path("", include(router.urls))
]
