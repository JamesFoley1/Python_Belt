# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-22 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_quotes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotes',
            name='likes',
        ),
        migrations.AddField(
            model_name='users',
            name='likes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]