# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 12:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demo', '0011_auto_20171021_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='maid',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
