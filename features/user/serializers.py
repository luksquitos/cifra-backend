from rest_framework import serializers, exceptions
from django.contrib.auth.hashers import make_password
from features.user import models
from django.utils.translation import gettext_lazy as _


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


class ChangeUserPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate_password2(self, value):
        if value != self.initial_data.get("password1"):
            raise exceptions.ValidationError(_("The two passwords do not match."))
        return value

    def save(self, **kwargs):
        request = self.context.get("request")
        user = request.user
        validated_data = self.validated_data

        user.password = make_password(validated_data.get("password1"))
        user.update_password = False
        user.save()

        return user
