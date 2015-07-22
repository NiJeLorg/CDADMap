# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0017_auto_20150720_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveypanel',
            name='Languages_Other',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
