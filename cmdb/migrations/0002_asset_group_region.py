# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2020-08-18 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='asset_Group_Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assetId', models.IntegerField(blank=True, verbose_name='实例ID')),
                ('assetGroupId', models.IntegerField(blank=True, verbose_name='主机组')),
                ('assetregionId', models.IntegerField(blank=True, verbose_name='region区域ID')),
            ],
        ),
    ]
