from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from features.lists import models
from features.stores.models import Product


class ListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.UserList
        fields = "__all__"
        read_only_fields = ["total_price", "best_store", "last_update"]


class UserListDefault:
    requires_context = True

    def __call__(self, field):
        return field.context["view"].get_related_list()


class ProductListSerializer(serializers.ModelSerializer):
    user_list = serializers.HiddenField(default=UserListDefault())

    def validate_name(self, value):
        products = Product.objects.filter(name=value)
        if not products.exists():
            raise serializers.ValidationError("Produto com este nome não existe")

        return value

    def create(self, validated_data):
        name = validated_data.get("name")
        product = Product.objects.filter(name=name).first()
        validated_data["image"] = product.image

        return super().create(validated_data)

    class Meta:
        model = models.ProductList
        fields = "__all__"
        read_only_fields = ["image"]
        validators = [
            UniqueTogetherValidator(
                queryset=models.ProductList.objects.all(),
                fields=["user_list", "name"],
                message="Produto já está nesta lista",
            )
        ]
