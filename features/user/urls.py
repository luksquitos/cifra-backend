from django.urls import path
from features.user import views

urlpatterns = [
    path("me/", views.AuthenticatedUserAPIView.as_view(), name="authenticated-user"),
]
