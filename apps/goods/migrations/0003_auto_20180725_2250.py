# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-25 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20180714_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookscategory',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='添加时间'),
        ),
    ]