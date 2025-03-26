from rest_framework import serializers
from features.products import models


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"