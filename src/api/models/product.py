from django.db import models

from api.models import TimeStampedModel, Type, User


def name_file(instance, filename):
    return '/'.join(['images', str(instance.provider_id.id), filename])


class Product(TimeStampedModel):
    provider_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    unit = models.CharField(max_length=255, null=True, blank=True)
    price_per_unit = models.PositiveIntegerField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    verify = models.CharField(max_length=255, null=True, blank=True)
    detail = models.TextField(max_length=10000, null=True, blank=True)
    image = models.ImageField(upload_to=name_file, max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
