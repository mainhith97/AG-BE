# Generated by Django 2.2.3 on 2019-10-07 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
