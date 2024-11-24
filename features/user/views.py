from rest_framework import views, status, response
from features.user import serializers
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


class ChangeUserPasswordAPIView(views.APIView):
    @extend_schema(
        responses={200: OpenApiResponse({}, description="Senha alterada com sucesso")},
        description="Altera a senha do usuário logado",
        request=serializers.ChangeUserPasswordSerializer,
    )
    def put(self, request):
        serializer = serializers.ChangeUserPasswordSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response()
