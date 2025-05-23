from django.contrib.auth import login
from django.shortcuts import redirect, render
from drf_spectacular.utils import extend_schema
from rest_framework import response, status, views

from features.user import forms, serializers


class AuthenticatedUserAPIView(views.APIView):
    @extend_schema(
        responses={
            200: serializers.UserSerializer,
        },
        description="Obtem os dados do usuário logado",
    )
    def get(self, request):
        serializer = serializers.UserSerializer(
            instance=request.user, context={"request": request}
        )
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class UserAPIView(views.APIView):
    @extend_schema(
        responses={
            200: serializers.CreateUserSerializer,
        },
        request=serializers.CreateUserSerializer,
        description="Cria um novo usuário do tipo cliente",
    )
    def post(self, request):
        serializer = serializers.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data, status=200)


def logistic_register_view(request):
    if request.method == "POST":
        form = forms.LogisticSignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("/admin/")
    else:
        form = forms.LogisticSignUpForm()

    return render(request, "sign-up-logistic.html", {"form": form})
