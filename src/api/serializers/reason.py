from rest_framework import serializers

from api.models import Reason


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', 'order_id', 'supplier_id', 'reason', 'created_at')
