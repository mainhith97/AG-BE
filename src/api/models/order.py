from django.core.validators import RegexValidator
from django.db import models
from rest_framework.compat import MinLengthValidator

from api.models import Product, TimeStampedModel, User


class Order(TimeStampedModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order', null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_order',
                                   null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    proposed_price = models.PositiveIntegerField(null=True, blank=True)
    datetime = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(validators=[MinLengthValidator(9),
                                             RegexValidator(regex='^\d+$', message='A valid integer is required.')],
                                 max_length=11, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, default='Pending')
