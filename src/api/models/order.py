from django.db import models

from api.models import Product, TimeStampedModel, User


class Order(TimeStampedModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order', null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_order',
                                   null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    proposed_price = models.PositiveIntegerField(null=True, blank=True)
    datetime = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, default='Đang chờ')
