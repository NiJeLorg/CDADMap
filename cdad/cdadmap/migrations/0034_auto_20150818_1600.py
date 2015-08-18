# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0033_auto_20150812_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partners',
            name='partner_name',
            field=models.CharField(default=b'', unique=True, max_length=255),
            preserve_default=True,
        ),
    ]
