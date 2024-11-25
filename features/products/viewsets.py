from rest_framework import viewsets
from features.products import serializers, models


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductsSerializer
    queryset = models.Product.objects.all()