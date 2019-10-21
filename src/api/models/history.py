from django.db import models
from rest_framework.compat import MinValueValidator, MaxValueValidator

from api.models import Product, TimeStampedModel, User


class History(TimeStampedModel):
    user_id = models.PositiveSmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    products = models.CharField(max_length=255, null=True, blank=True)
    totals = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, default='Đang chờ')
