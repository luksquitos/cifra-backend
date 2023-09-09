from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from ..models import Market, Product, ProductImage
from .serializers import (
    MarketAdminSerializer, 
    ProductAdminSerializer,
    ProductImageAdminSerializer
)


class MarketAdminViewset(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Market.objects.all()
    serializer_class = MarketAdminSerializer


class ProductAdminViewset(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductAdminSerializer


class ProductImageAdminViewset(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageAdminSerializer


