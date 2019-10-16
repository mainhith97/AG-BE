from rest_framework import serializers

from api.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user_id', 'product_id',
                  'quantity', 'proposed_price', 'datetime', 'status')
