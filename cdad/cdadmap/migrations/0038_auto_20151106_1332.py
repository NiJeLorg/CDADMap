# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0037_auto_20151106_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveypanel',
            name='instagram',
            field=models.URLField(max_length=2000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='surveypanel',
            name='nextdoor',
            field=models.URLField(max_length=2000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='surveypanel',
            name='youtube',
            field=models.URLField(max_length=2000, null=True, blank=True),
        ),
    ]
