from django.db import models

from api.models import TimeStampedModel, User, Order


class Reason(TimeStampedModel):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order', null=True, blank=True)
    supplier_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supplier',
                                    null=True, blank=True)
    reason = models.TextField(max_length=10000, null=True, blank=True)
