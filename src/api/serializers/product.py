from rest_framework import serializers

from api.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'provider_id', 'unit', 'price_per_unit',
                  'in_stock', 'type', 'description', 'verify', 'detail', 'image')


class ProductPopular(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'unit', 'price_per_unit', 'image')
