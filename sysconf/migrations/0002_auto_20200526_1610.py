# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2020-05-26 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysconf', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ossconf',
            old_name='bucketname',
            new_name='bucketName',
        ),
        migrations.AlterField(
            model_name='sys_menu',
            name='component',
            field=models.CharField(max_length=300, null=True, verbose_name='component地址'),
        ),
        migrations.AlterField(
            model_name='sys_menu',
            name='del_flag',
            field=models.IntegerField(choices=[(0, '删除'), (1, '正常')], default=1, verbose_name='逻辑删除 0-删除， 1-正常'),
        ),
        migrations.AlterField(
            model_name='sys_menu',
            name='hidden',
            field=models.IntegerField(choices=[(0, '否'), (1, '是')], default=0, verbose_name='是否隐藏路由: 0-否,1-是'),
        ),
        migrations.AlterField(
            model_name='sys_menu',
            name='keep_alive',
            field=models.IntegerField(choices=[(0, '关闭'), (1, '开启')], default=1, verbose_name='0-关闭，1- 开启'),
        ),
        migrations.AlterField(
            model_name='sys_menu',
            name='perssion',
            field=models.CharField(max_length=300, null=True, verbose_name='菜单权限标识'),
        ),
        migrations.AlterField(
            model_name='sys_menu',
            name='redirect',
            field=models.CharField(max_length=300, null=True, verbose_name='重定向地址'),
        ),
        migrations.AlterField(
            model_name='sys_menu',
            name='target',
            field=models.CharField(max_length=300, null=True, verbose_name='连接跳转目标'),
        ),
        migrations.AlterField(
            model_name='sys_menu',
            name='type',
            field=models.IntegerField(choices=[(0, '菜单'), (1, '按钮')], default=0, verbose_name='菜单类型 （0-菜单 1-按钮'),
        ),
        migrations.AlterField(
            model_name='sys_menu',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
    ]
