# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2020-06-17 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysconf', '0005_auto_20200606_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='baseConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='配置名称')),
                ('confKey', models.CharField(max_length=50, verbose_name='配置键')),
                ('confValue', models.CharField(max_length=50, verbose_name='配置值')),
                ('category', models.CharField(blank=True, max_length=255, verbose_name='分类')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='描述')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.RenameField(
            model_name='sys_alarm_log',
            old_name='create_time',
            new_name='createTime',
        ),
        migrations.RenameField(
            model_name='sys_role',
            old_name='create_time',
            new_name='createTime',
        ),
        migrations.RenameField(
            model_name='sys_role',
            old_name='update_time',
            new_name='updateTime',
        ),
        migrations.RenameField(
            model_name='sys_webhoook',
            old_name='create_time',
            new_name='createTime',
        ),
        migrations.RenameField(
            model_name='sys_webhoook',
            old_name='update_time',
            new_name='updateTime',
        ),
        migrations.AddField(
            model_name='sys_alarm_log',
            name='updateTime',
            field=models.DateTimeField(default='', verbose_name='更新时间'),
            preserve_default=False,
        ),
    ]