# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-17 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20180725_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='添加时间'),
        ),
    ]
