# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 02:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20171004_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='key_words',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='key words'),
        ),
    ]