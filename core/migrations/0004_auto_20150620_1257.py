# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150619_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='geotag',
            name='symbol',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='papertag',
            name='symbol',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phase',
            name='symbol',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
