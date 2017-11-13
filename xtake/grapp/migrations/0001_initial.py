# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 15:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('party', models.CharField(max_length=10)),
                ('region', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Promise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grapp.Candidate')),
                ('related', models.ManyToManyField(blank=True, related_name='_promise_related_+', to='grapp.Promise')),
            ],
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_advantage', models.BooleanField()),
                ('message', models.TextField()),
                ('keywords', jsonfield.fields.JSONField()),
                ('selected_promise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_promise', to='grapp.Promise')),
                ('shown_promise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shown_promise', to='grapp.Promise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grapp.Election'),
        ),
    ]