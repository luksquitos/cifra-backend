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
