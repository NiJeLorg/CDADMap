# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0029_auto_20150722_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveypanel',
            name='removed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
