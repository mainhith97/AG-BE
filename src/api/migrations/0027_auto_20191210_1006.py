# Generated by Django 2.2.3 on 2019-12-10 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20191210_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
    ]
