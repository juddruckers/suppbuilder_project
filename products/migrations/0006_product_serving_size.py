# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 02:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20161201_0432'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='serving_size',
            field=models.CharField(default='100 mg', max_length=120),
        ),
    ]
