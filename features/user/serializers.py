from rest_framework import serializers

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


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer used to create a new Client"""

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_confirm_password(self, value):
        password = self.initial_data.get("password")

        if value != password:
            raise serializers.ValidationError("As senhas informadas não são iguais")

        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        return models.User.objects.create_user(**validated_data)

    class Meta:
        model = models.User
        fields = ["confirm_password", "password", "email", "name"]
