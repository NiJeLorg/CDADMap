# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0006_auto_20141216_1651'),
    ]

    operations = [
        migrations.RenameField(
            model_name='locationpanel',
            old_name='Organization_Name_FK',
            new_name='Organization_Name_SurveyPanel_FK',
        ),
        migrations.RemoveField(
            model_name='contactpanel',
            name='Organization_Name_FK',
        ),
        migrations.RemoveField(
            model_name='meetingpanel',
            name='Organization_Name_FK',
        ),
        migrations.AddField(
            model_name='locationpanel',
            name='Organization_Name_ContactPanel_FK',
            field=models.ForeignKey(to='cdadmap.ContactPanel', to_field=b'Organization_Name', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpanel',
            name='Organization_Name',
            field=models.TextField(unique=True),
            preserve_default=True,
        ),
    ]
