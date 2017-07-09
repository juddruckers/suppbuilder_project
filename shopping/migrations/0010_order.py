# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-07 01:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0009_auto_20170619_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=120)),
            ],
        ),
    ]
