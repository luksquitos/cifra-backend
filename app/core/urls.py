"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from markets.api.viewsets import MarketViewset, ProductViewset
from markets.admin_api.viewsets import (
    MarketAdminViewset,
    ProductAdminViewset,
    ProductImageAdminViewset
)


router = DefaultRouter()
router.register("markets", MarketViewset, "Markets")
router.register("products", ProductViewset, "Products")
#admin-api
router.register("admin-api/markets", MarketAdminViewset, "MarketAdmin")
router.register("admin-api/products", ProductAdminViewset, "ProductAdmin")
router.register("admin-api/products-images", ProductImageAdminViewset, "ProductImageAdmin")


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path(
        'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path(
        'api-auth/', include("rest_framework.urls", namespace="rest_framework")
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
