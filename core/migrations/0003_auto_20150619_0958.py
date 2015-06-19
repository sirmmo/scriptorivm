# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150619_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geom',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='phase',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
