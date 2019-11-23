from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api.models import Product, TimeStampedModel, User


class Cart(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_user', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product', null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
