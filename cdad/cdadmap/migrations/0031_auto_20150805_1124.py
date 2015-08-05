# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0030_surveypanel_removed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingpanel',
            name='repeat',
            field=models.CharField(default=b'NEVER', max_length=15, choices=[(b'NEVER', b'Never'), (b'DAILY', b'Every Day'), (b'WEEKDAY', b'Every Weekday'), (b'WEEKLY', b'Every Week'), (b'MONTHLY', b'Every Month'), (b'YEARLY', b'Every Year')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='Social_Twitter',
            field=models.URLField(max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='Social_facebook',
            field=models.URLField(max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='Social_website',
            field=models.URLField(max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
