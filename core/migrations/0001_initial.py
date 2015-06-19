# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Geom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GeoTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.URLField()),
                ('title', models.TextField()),
                ('abstract', models.TextField()),
                ('publication_date', models.DateField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('refers_to_geometry', models.ForeignKey(related_name='researches', to='core.Geom')),
            ],
        ),
        migrations.CreateModel(
            name='PaperTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('year_from', models.IntegerField()),
                ('year_to', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='paper',
            name='refers_to_period',
            field=models.ForeignKey(to='core.Phase'),
        ),
        migrations.AddField(
            model_name='paper',
            name='tags',
            field=models.ManyToManyField(to='core.PaperTag'),
        ),
        migrations.AddField(
            model_name='geom',
            name='tags',
            field=models.ManyToManyField(to='core.GeoTag'),
        ),
    ]
