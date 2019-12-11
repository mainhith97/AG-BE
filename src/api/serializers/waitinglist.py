from rest_framework import serializers

from api.models import Waitinglist


class WaitinglistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitinglist
        fields = ('id', 'user', 'product')
