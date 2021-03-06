# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-23 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_product_sku'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('email', models.EmailField(max_length=120)),
                ('code', models.CharField(max_length=120)),
            ],
        ),
    ]
