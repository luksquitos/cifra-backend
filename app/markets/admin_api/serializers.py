from rest_framework import serializers
from ..models import Market, Product, ProductImage


class MarketAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = "__all__"


class ProductAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductImageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


