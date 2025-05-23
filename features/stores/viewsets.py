from django.db.models import F, OuterRef, Subquery
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.filters import ParameterizedFilterBackend, SearchFilter
from features.stores import models, serializers


@extend_schema(tags=["products"])
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.select_related("category").all()
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


@extend_schema(tags=["historic"])
class ProductHistoricViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoint que lida com os históricos de preços dos produtos"""

    serializer_class = serializers.PriceHistorySerializer
    filter_backends = (ParameterizedFilterBackend,)
    filter_params_query = {"start_at": "created_at__gte", "end_at": "created_at__lte"}

    def get_queryset(self):
        pk = self.kwargs.get("product_pk")

        return models.PriceProductHistory.objects.select_related("product").filter(
            product__pk=pk
        )

    @action(methods=["get"], detail=False)
    def last(self, request, product_pk):
        """Retorna o preço atual do produto"""
        current_price = self.get_queryset().first()
        serializer = self.get_serializer(instance=current_price)

        return Response(serializer.data, 200)


@extend_schema(tags=["characteristics"])
class ProductCharacteristicsViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoint que lida com as caraterísticas técnicas dos produtos"""

    serializer_class = serializers.PriceCharacteristicsSerializer

    def get_queryset(self):
        pk = self.kwargs.get("product_pk")

        return models.ProductTechnicalCharacteristics.objects.select_related(
            "product"
        ).filter(product__pk=pk)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="width", type=OpenApiTypes.STR, description="Largura do SVG"
            ),
            OpenApiParameter(
                name="height", type=OpenApiTypes.STR, description="Altura do SVG"
            ),
            OpenApiParameter(
                name="fill_svg", type=OpenApiTypes.STR, description="Cor do SVG"
            ),
            OpenApiParameter(
                name="fill_path",
                type=OpenApiTypes.STR,
                description="Cor do path do SVG",
            ),
        ]
    )
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CategorySvgSerializer
    queryset = models.Category.objects.all()
    pagination_class = None
