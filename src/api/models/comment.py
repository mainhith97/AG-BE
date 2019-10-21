from django.db import models

from api.models import Product, TimeStampedModel, User


class Comment(TimeStampedModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cmt', null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cmt',
                                   null=True, blank=True)
    comment = models.TextField(max_length=10000, null=True, blank=True)
