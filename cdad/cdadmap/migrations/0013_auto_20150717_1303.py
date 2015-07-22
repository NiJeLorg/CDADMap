# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0012_surveypanel_organization_logo_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactpanel',
            name='KeepPrivate',
        ),
        migrations.AddField(
            model_name='contactpanel',
            name='KeepPrivateEmail',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactpanel',
            name='KeepPrivateTel',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contactpanel',
            name='AddListPermission',
            field=models.BooleanField(),
            preserve_default=True,
        ),
    ]
