from rest_framework import serializers
from ..models import Market, Product, ProductImage


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["product"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(read_only=True, many=True) #FIXME Is there a easy way ?!
    class Meta:
        model = Product
        fields = "__all__"