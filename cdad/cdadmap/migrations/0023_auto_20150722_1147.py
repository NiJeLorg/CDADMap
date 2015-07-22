# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0022_auto_20150721_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingpanel',
            name='Address2',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='accomplish_five_description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='accomplish_five_title',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='accomplish_four_description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='accomplish_four_title',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='accomplish_three_description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='accomplish_three_title',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='accomplish_two_description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='surveypanel',
            name='accomplish_two_title',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
