# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-25 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('inventory', models.IntegerField(default=0)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Clothing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('small', models.IntegerField(default=0)),
                ('medium', models.IntegerField(default=0)),
                ('large', models.IntegerField(default=0)),
                ('xlarge', models.IntegerField(default=0)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clothingType', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=5)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('user', models.CharField(max_length=100)),
                ('cash', models.FloatField()),
            ],
        ),
    ]
