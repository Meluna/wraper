# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 12:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='HDD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('image', models.TextField()),
                ('description', models.TextField()),
                ('page', models.TextField()),
                ('price', models.IntegerField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Libwrapp.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Speed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='hdd',
            name='interface',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Libwrapp.Interface'),
        ),
        migrations.AddField(
            model_name='hdd',
            name='speed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Libwrapp.Speed'),
        ),
        migrations.AddField(
            model_name='hdd',
            name='volume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Libwrapp.Volume'),
        ),
    ]
