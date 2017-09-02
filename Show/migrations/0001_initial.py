# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='odlinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('odlname', models.CharField(max_length=30)),
                ('odlip', models.CharField(max_length=20)),
                ('odlport', models.CharField(max_length=10)),
                ('odlkey', models.CharField(max_length=20)),
                ('odlright', models.CharField(max_length=10)),
                ('odlstate', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='odlsetlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logtime', models.DateField()),
                ('loginfo', models.CharField(max_length=100)),
            ],
        ),
    ]
