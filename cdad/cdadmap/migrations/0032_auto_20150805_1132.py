# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0031_auto_20150805_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveypanel',
            name='Social_Phone',
            field=models.CharField(default=b'', max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='surveypanel',
            name='Social_Phone_KeepPrivate',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
