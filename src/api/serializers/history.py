from rest_framework import serializers

from api.models import History


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = (
        'id', 'user_id', 'name', 'products', 'totals', 'created_at', 'address', 'telephone', 'status')
