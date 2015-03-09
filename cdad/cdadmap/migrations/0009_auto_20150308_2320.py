# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0008_auto_20150212_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationpanel',
            name='Organization_Name_ContactPanel_FK',
        ),
        migrations.AddField(
            model_name='locationpanel',
            name='Organization_Name_ContactPanel',
            field=models.ManyToManyField(to='cdadmap.ContactPanel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locationpanel',
            name='Organization_Name_MeetingPanel',
            field=models.ManyToManyField(to='cdadmap.MeetingPanel', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpanel',
            name='Organization_Name',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
