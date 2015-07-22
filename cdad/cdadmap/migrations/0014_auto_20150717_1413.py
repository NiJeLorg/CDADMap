# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0013_auto_20150717_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpanel',
            name='AddListPermission',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpanel',
            name='KeepPrivateEmail',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpanel',
            name='KeepPrivateTel',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
