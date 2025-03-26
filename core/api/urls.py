from django.urls import path, include, reverse
from django.shortcuts import redirect

urlpatterns = [
    path("auth/", include("features.authentication.urls")),
    path("docs/", include("core.swagger.urls")),
    path("users/", include("features.user.urls")),
    path("", lambda x: redirect(reverse("swagger-ui"))),
]
