from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import MarketSerializer, ProductSerializer, ProductImageSerializer
from ..models import Market, Product


class MarketViewset(ReadOnlyModelViewSet):
    serializer_class = MarketSerializer
    queryset = Market.objects.all()


class ProductViewset(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["market"]
    search_fields = ["name"]
    ordering_fields = ["price"]

