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

    @action(methods=["put"], detail=True)
    def calculate(self, request, pk):
        pass
        # user_list = self.get_object()
        # user_list.calculate_best_spot()

        return Response(status=200)


class ProductListViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductListSerializer
    permission_classes = [IsAuthenticated]

    # Imagino que para criar, não terá validação por usuário.
    def get_queryset(self, request):
        pk = self.kwargs.get("list_pk")
        return models.ProductList.objects.select_related("user_list__user").filter(
            user_list__pk=pk, user_list__user=self.request.user
        )
