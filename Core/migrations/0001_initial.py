# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-30 00:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='media_dir/%Y/%m/%d/%S')),
                ('description', models.CharField(blank=True, max_length=50)),
                ('key', models.SlugField(default='Wgt8', max_length=4, unique=True)),
                ('uploadTime', models.DateTimeField(default=datetime.datetime(2016, 7, 30, 3, 34, 11, 678521))),
                ('lastViewTime', models.DateTimeField(default=datetime.datetime(2016, 7, 30, 3, 34, 11, 678521))),
                ('viewCounter', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['-uploadTime'],
            },
        ),
    ]
