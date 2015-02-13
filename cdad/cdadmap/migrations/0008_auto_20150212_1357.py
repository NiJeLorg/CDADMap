# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0007_auto_20141216_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationpanel',
            name='Lat',
            field=models.CharField(default=b'', max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locationpanel',
            name='Lon',
            field=models.CharField(default=b'', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
