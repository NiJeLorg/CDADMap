# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0035_auto_20150921_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveypanel',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 18, 50, 32, 531842, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='surveypanel',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 18, 50, 37, 525720, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
