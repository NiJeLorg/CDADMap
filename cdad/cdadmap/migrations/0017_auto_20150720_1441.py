# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0016_locationpanel_councildistricts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationpanel',
            name='CouncilDistricts',
        ),
        migrations.AddField(
            model_name='surveypanel',
            name='CouncilDistricts',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
