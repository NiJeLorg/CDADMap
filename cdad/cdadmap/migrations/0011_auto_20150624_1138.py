# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cdadmap', '0010_auto_20150308_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveypanel',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='surveypanel',
            name='verified',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
