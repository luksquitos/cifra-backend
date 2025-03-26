from rest_framework import views, status, response
from features.user import serializers, models
from drf_spectacular.utils import extend_schema, OpenApiResponse

class AuthenticatedUserAPIView(views.APIView):
    @extend_schema(
        responses={
            200: serializers.UserSerializer,
        },
        description="Obtem os dados do usuário logado",
    )
    def get(self, request):
        serializer = serializers.UserSerializer(instance=request.user, context={'request':request})
        return response.Response(serializer.data, status=status.HTTP_200_OK)
