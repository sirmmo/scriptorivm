# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='refers_to_geometry',
        ),
        migrations.AddField(
            model_name='paper',
            name='refers_to_geometry',
            field=models.ManyToManyField(related_name='researches', to='core.Geom'),
        ),
    ]
