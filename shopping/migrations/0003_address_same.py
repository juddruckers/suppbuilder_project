# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-05 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0002_auto_20170105_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='same',
            field=models.BooleanField(default=False),
        ),
    ]
