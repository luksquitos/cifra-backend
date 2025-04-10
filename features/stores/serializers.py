from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class CategorySvgSerializer(serializers.ModelSerializer):
    svg = serializers.SerializerMethodField()

    def get_svg(self, obj: models.Category):
        query_params = self.context.get("request").query_params
        query_params = self._format_query_params(query_params)

        obj.update_svg_attributes(**query_params)

        return obj.svg

    def _format_query_params(self, query_params):
        params_formatted = {}

        for key in query_params:
            params_formatted[key] = query_params.get(key)

        return params_formatted

    class Meta:
        model = models.Category
        fields = "__all__"
