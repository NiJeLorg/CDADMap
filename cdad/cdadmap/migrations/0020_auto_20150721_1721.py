# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0019_auto_20150721_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingpanel',
            name='hasMeeting',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
