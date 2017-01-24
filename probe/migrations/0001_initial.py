# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-13 11:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AverageQuality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('avg_download', models.IntegerField(db_column='avg_download', help_text='Download Speed in Bit/s')),
                ('avg_upload', models.IntegerField(db_column='avg_upload', help_text='Upload Speed in Bit/s')),
            ],
            options={
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_upload', models.IntegerField(db_column='upload')),
                ('expected_download', models.IntegerField(db_column='download')),
                ('prtg_url', models.URLField(blank=True, db_column='prtg_url')),
                ('prtg_token', models.CharField(blank=True, db_column='prtg_token', max_length=255)),
            ],
            options={
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='Speed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('server', models.CharField(db_column='server', help_text='Server Location', max_length=255)),
                ('ping', models.IntegerField(db_column='ping', help_text='Ping in ms')),
                ('download', models.IntegerField(db_column='download', help_text='Download Speed in Bit/s')),
                ('upload', models.IntegerField(db_column='upload', help_text='Upload Speed in Bit/s')),
            ],
            options={
                'get_latest_by': 'id',
            },
        ),
    ]