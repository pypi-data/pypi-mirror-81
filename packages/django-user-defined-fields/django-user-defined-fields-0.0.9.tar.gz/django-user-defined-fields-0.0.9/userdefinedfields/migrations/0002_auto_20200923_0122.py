# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-23 01:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userdefinedfields', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extrafield',
            old_name='required',
            new_name='is_required',
        ),
    ]
