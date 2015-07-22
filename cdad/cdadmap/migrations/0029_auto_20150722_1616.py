# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0028_auto_20150722_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveypanel',
            name='CDAD_Comments',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='CDAD_FeedBack',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
