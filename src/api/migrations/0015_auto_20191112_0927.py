# Generated by Django 2.2.3 on 2019-11-12 02:27

import django.core.validators
from django.db import migrations, models
import rest_framework.compat


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20191106_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='telephone',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[rest_framework.compat.MinLengthValidator(9), django.core.validators.RegexValidator(message='A valid integer is required.', regex='^\\d+$')]),
        ),
    ]
