from rest_framework import serializers

from features.lists import models


class ListSerializer(serializers.ModelSerializer):
    # Need to be null values?
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    # better_store = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.UserList
        fields = "__all__"
        read_only_fields = ["total_price", "better_store", "last_update"]


class ProductListSerializer(serializers.ModelSerializer):
    # user_list = serializers.HiddenField("default") # Tem que pegar do NestedRouter

    class Meta:
        model = models.ProductList
        fields = "__all__"
