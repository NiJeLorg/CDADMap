# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0009_auto_20150308_2320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='locationpanel',
            old_name='Organization_Name_ContactPanel',
            new_name='Organization_Name_ContactPanel_M2M',
        ),
        migrations.RenameField(
            model_name='locationpanel',
            old_name='Organization_Name_MeetingPanel',
            new_name='Organization_Name_MeetingPanel_M2M',
        ),
    ]
