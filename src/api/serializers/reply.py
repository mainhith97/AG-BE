from rest_framework import serializers

from api.models import Reply


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('id', 'cmt_id', 'provider_id', 'reply', 'created_at')
