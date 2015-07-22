# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0015_auto_20150719_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationpanel',
            name='CouncilDistricts',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
