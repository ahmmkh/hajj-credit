# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-02 01:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('pwd', models.CharField(max_length=200)),
                ('logged_in', models.BooleanField(default=False)),
            ],
        ),
    ]