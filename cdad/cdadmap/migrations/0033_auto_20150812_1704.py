# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0032_auto_20150805_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveypanel',
            name='Organization_Name',
            field=models.CharField(default=b'', unique=True, max_length=2000),
            preserve_default=True,
        ),
    ]
