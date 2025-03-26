from rest_framework import serializers, exceptions
from django.contrib.auth.hashers import make_password
from features.user import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = [
            "password",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        ]