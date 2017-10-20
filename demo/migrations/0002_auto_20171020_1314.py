# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-20 07:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('educational_profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='demo.Educational_Profile')),
                ('general_profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='demo.General_Profile')),
                ('job_profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='demo.JobProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Other_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_issue', models.CharField(max_length=1000, null=True)),
                ('current_salary', models.FloatField(null=True)),
                ('expected_salary', models.FloatField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='maid',
            name='other_details',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='demo.Other_Details'),
        ),
        migrations.AddField(
            model_name='maid',
            name='skills',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='demo.Skills'),
        ),
        migrations.AddField(
            model_name='maid',
            name='uploads',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='demo.Uploads'),
        ),
    ]
