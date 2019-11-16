from django.db import models

from api.models import TimeStampedModel, User, Comment


class Reply(TimeStampedModel):
    cmt_id = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='cmt', null=True, blank=True)
    provider_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider',
                                    null=True, blank=True)
    reply = models.TextField(max_length=10000, null=True, blank=True)
