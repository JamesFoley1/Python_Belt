# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-22 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0005_remove_users_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='my_like',
            field=models.BooleanField(default=False),
        ),
    ]
