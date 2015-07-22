# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0026_auto_20150722_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveypanel',
            name='CDAD_Services_Other',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
