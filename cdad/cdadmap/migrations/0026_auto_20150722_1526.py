# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0025_auto_20150722_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveypanel',
            name='partners',
            field=models.ManyToManyField(to='cdadmap.Partners', null=True, blank=True),
            preserve_default=True,
        ),
    ]
