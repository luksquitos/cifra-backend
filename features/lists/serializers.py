from rest_framework import serializers

from features.lists import models


class ListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.UserList
        fields = "__all__"
        read_only_fields = ["total_price", "better_store", "last_update"]


class UserListDefault:
    requires_context = True

    def __call__(self, field):
        return field.context["view"].get_related_list()


class ProductListSerializer(serializers.ModelSerializer):
    user_list = serializers.HiddenField(default=UserListDefault())

    class Meta:
        model = models.ProductList
        fields = "__all__"
