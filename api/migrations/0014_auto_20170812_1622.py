# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-12 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20170810_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='aeName',
            field=models.CharField(choices=[('ae-smarts', 'ae-smarts'), ('ae-smarts', 'ae-smarts'), ('ae-smarts', 'ae-smarts'), ('ae-smarts', 'ae-smarts')], default='ae-smarts', max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='cntName',
            field=models.CharField(choices=[('cnt-led', 'cnt-led'), ('cnt-ultra', 'cnt-ultra'), ('cnt-dht', 'cnt-dht'), ('cnt-hue', 'cnt-hue')], default='cnt-led', max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='deviceCom',
            field=models.CharField(choices=[('smArts', 'smArts'), ('Philips', 'Philips')], default='smArts', max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='deviceName',
            field=models.CharField(choices=[('led', 'LED전등'), ('ultra', '초음파감지기'), ('humidity', '온습도측정'), ('hue', 'hue')], default='led', max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='deviceType',
            field=models.CharField(choices=[('bulb', '전등'), ('ultrasensor', '초음파센서'), ('humiditysensor', '온습도센서'), ('bulb', '전등')], default='bulb', max_length=255),
        ),
    ]
