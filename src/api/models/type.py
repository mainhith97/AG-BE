from django.db import models

from api.models import TimeStampedModel


class Type(TimeStampedModel):
    product_type = models.CharField(max_length=255)
