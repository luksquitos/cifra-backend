from django.db.models import F, OuterRef, Subquery
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.filters import ParameterizedFilterBackend, SearchFilter
from features.stores import models, serializers


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.select_related("category").all()
    permission_classes = []
    filter_backends = [ParameterizedFilterBackend, SearchFilter]
    filter_params_query = {
        "category": "category",
    }
    search_fields = ["name"]

    @action(detail=False, methods=["get"])
    def promotions(self, request):
        queryset = self.queryset.annotate(
            lowest_price=Subquery(
                self.queryset.filter(name=OuterRef("name")).values("price")[:1]
            )
        ).filter(price=F("lowest_price"))

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    permission_classes = []
