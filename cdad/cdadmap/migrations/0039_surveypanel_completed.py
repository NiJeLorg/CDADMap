# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0038_auto_20151106_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveypanel',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
