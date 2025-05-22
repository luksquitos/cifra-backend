from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.urls import include, path, reverse

from core.admin import site
from features.user.views import logistic_register_view


urlpatterns = [
    path("sign-up/", logistic_register_view, name="logistic-register"),
    path("admin/", site.urls),
    path("api/", include("core.api.urls")),
    path("", lambda x: redirect(reverse("swagger-ui"))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
