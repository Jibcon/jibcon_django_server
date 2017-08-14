# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-14 02:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_routine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='deviceName',
            field=models.CharField(choices=[('led', 'LED전등'), ('ultra', '초음파감지기'), ('humidity', '온습도측정'), ('Philips Hue 전구', 'hue')], default='led', max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='deviceType',
            field=models.CharField(choices=[('bulb', '전등'), ('ultrasensor', '초음파센서'), ('humiditysensor', '온습도센서'), ('hue-bulb', '전등')], default='bulb', max_length=255),
        ),
    ]
