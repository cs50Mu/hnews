# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-11 10:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20181210_0047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='source',
        ),
    ]
