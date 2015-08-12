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
        migrations.AlterField(
            model_name='contactpanel',
            name='Organization_Name',
            field=models.CharField(default=b'', unique=True, max_length=255),
            preserve_default=True,
        ),    
    ]
