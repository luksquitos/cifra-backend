from rest_framework import serializers
from features.address import models


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        exclude = ["id"]
