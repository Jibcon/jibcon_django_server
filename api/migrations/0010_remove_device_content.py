# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-09 04:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_device_devicewifiaddr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='content',
        ),
    ]
