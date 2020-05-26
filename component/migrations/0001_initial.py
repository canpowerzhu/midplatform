# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2020-05-26 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='apklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectName', models.CharField(blank=True, max_length=500, null=True, verbose_name='项目名称')),
                ('packageName', models.CharField(blank=True, max_length=500, null=True, verbose_name='apk包名')),
                ('version', models.IntegerField(verbose_name='版本号')),
                ('envType', models.IntegerField(choices=[(0, '正式环境'), (1, '测试环境')], verbose_name='正式环境-0 测试环境-1')),
                ('size', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='apk文件大小， 单位为MB')),
                ('owner', models.CharField(max_length=100, verbose_name='提交人')),
                ('url', models.CharField(max_length=300, verbose_name='apk下载地址')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='apklist',
            unique_together=set([('packageName', 'version', 'envType')]),
        ),
    ]
