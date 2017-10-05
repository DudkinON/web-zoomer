# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 07:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_languages'),
        ('blog', '0010_auto_20171005_0541'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=255, verbose_name='title')),
                ('key_words', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='key words')),
                ('description', models.TextField(default=None, verbose_name='description')),
                ('text', models.TextField(default=None, verbose_name='text')),
                ('slug', models.CharField(default=None, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('views', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('image', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blog.ArticleImage')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(default=None, max_length=65, verbose_name='tag')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('language', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.Languages')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.RemoveField(
            model_name='blog',
            name='author',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='category',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='image',
        ),
        migrations.RemoveField(
            model_name='category',
            name='language',
        ),
        migrations.AlterField(
            model_name='articlelikes',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article'),
        ),
        migrations.DeleteModel(
            name='Blog',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blog.ArticleTag'),
        ),
    ]
