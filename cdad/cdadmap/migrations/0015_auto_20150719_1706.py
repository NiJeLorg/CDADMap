# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0014_auto_20150717_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationpanel',
            name='KeepPrivate',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locationpanel',
            name='MailingAddress',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
