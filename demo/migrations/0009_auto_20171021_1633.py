# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0008_auto_20171020_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobprofile',
            name='job_experience',
            field=models.ManyToManyField(null=True, to='demo.JobExperience'),
        ),
    ]
