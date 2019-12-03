from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from api.models import TimeStampedModel


class History(TimeStampedModel):
    user_id = models.PositiveSmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    products = models.CharField(max_length=255, null=True, blank=True)
    totals = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(validators=[MinLengthValidator(9),
                                             RegexValidator(regex='^\d+$', message='A valid integer is required.')],
                                 max_length=11, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, default='Pending')

