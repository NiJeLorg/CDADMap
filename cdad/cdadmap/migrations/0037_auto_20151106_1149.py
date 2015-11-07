# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0036_auto_20151105_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationpanel',
            name='Activity_Other',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='surveypanel',
            name='Organization_Description_Other',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='surveypanel',
            name='Service_Population_Other',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='CDAD_Services_Other',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
    ]
