# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-12 07:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0015_auto_20170812_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='현관문에 사람이 지나가면 Phillips Hue 전구를 켜줘.', max_length=255)),
                ('conditionMethod', models.CharField(choices=[('larger', '>'), ('smaller', '<'), ('equal', '=')], default='smArts', max_length=255)),
                ('value', models.CharField(default='0.1', max_length=255)),
                ('unit', models.CharField(default='m', max_length=255)),
                ('actuator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_routine_related_actuator', to='api.Device')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_routine_related_sensor', to='api.Device')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
