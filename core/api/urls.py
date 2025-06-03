from django.shortcuts import redirect
from django.urls import include, path, reverse

urlpatterns = [
    path("auth/", include("features.authentication.urls")),
    path("docs/", include("core.swagger.urls")),
    path("users/", include("features.user.urls")),
    path("lists/", include("features.lists.urls")),
    path("stores/", include("features.stores.urls")),
    path("", lambda x: redirect(reverse("swagger-ui"))),
]
