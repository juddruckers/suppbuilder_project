# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-26 04:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_order_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(default='sku default', max_length=120),
            preserve_default=False,
        ),
    ]
