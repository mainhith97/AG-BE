from django.db import models

from api.models import Product, TimeStampedModel, User


class Waitinglist(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_waiting_list', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_waiting_list', null=True,
                                blank=True)
