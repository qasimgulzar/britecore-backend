# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-03 18:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fieldvalues',
            unique_together=set([('entity_id', 'field')]),
        ),
    ]