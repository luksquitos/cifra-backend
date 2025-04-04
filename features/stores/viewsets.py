from rest_framework import viewsets

from core.filters import ParameterizedFilterBackend, SearchFilter
from features.stores import models, serializers


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = []
    filter_backends = [ParameterizedFilterBackend, SearchFilter]
    filter_params_query = {
        "category": "category",
    }
    
    search_fields = ["name"]
    
    # def get_queryset(self):
    #     return models.Product.objects.all().distinct("name")

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CategorySerializer 
    queryset = models.Category.objects.all()
    permission_classes = []