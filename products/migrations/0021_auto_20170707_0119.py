# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-07 01:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount',
            field=models.DecimalField(decimal_places=0, max_digits=6),
        ),
    ]
