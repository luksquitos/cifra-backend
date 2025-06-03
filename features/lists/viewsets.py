from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from features.lists import models, serializers


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.UserList.objects.select_related("user").filter(
            user=self.request.user
        )

    @extend_schema(
        request=None,
        description="Endpoint para calcular, ou recalcular, valor total de lista de usuário.",
        responses={200: {}},
    )
    @action(methods=["put"], detail=True)
    def calculate(self, request, pk):
        user_list = self.get_object()
        user_list.calculate_best_spot()

        return Response(status=200)


class ProductListViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.ProductList.objects.select_related("user_list__user").filter(
            user_list=self.get_related_list()
        )

    def get_related_list(self):
        return get_object_or_404(
            models.UserList, pk=self.kwargs.get("list_pk"), user=self.request.user
        )
