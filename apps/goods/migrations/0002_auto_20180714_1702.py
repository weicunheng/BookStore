# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-14 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishers',
            name='image',
            field=models.ImageField(max_length=200, upload_to='companylogo'),
        ),
    ]
