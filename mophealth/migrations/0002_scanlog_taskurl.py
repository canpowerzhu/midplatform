# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2020-06-28 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mophealth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanlog',
            name='taskUrl',
            field=models.CharField(default='', max_length=500, verbose_name='监控任务地址'),
            preserve_default=False,
        ),
    ]
