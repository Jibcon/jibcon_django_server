# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 16:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='deviceCom',
            field=models.CharField(default='찬주 일렉트로닉스', max_length=255),
        ),
        migrations.AddField(
            model_name='device',
            name='deviceName',
            field=models.CharField(default='동그라미플러그', max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='deviceType',
            field=models.CharField(default='에어컨', max_length=255),
        ),
    ]
