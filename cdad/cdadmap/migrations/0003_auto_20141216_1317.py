# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0002_auto_20141202_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveypanel',
            name='Organization_Name',
            field=models.CharField(default=b'', unique=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactpanel',
            name='Organization_Name_FK',
            field=models.ForeignKey(to='cdadmap.SurveyPanel', to_field=b'Organization_Name', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locationpanel',
            name='Organization_Name_FK',
            field=models.ForeignKey(to='cdadmap.SurveyPanel', to_field=b'Organization_Name', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meetingpanel',
            name='Organization_Name_FK',
            field=models.ForeignKey(to='cdadmap.SurveyPanel', to_field=b'Organization_Name', null=True),
            preserve_default=True,
        ),
    ]
