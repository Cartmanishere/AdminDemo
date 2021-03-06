# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-22 11:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demo', '0014_auto_20171022_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_option', models.CharField(choices=[('Cash', 'Cash'), ('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Online Payment', 'Online Payment'), ('Cheque', 'Cheque')], max_length=100)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], max_length=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('maid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.Maid')),
            ],
        ),
    ]
