# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0003_auto_20141216_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactpanel',
            name='Organization_Name_FK',
        ),
        migrations.RemoveField(
            model_name='locationpanel',
            name='Organization_Name_FK',
        ),
        migrations.RemoveField(
            model_name='meetingpanel',
            name='Organization_Name_FK',
        ),
        migrations.AlterField(
            model_name='contactpanel',
            name='Organization_Name',
            field=models.ForeignKey(to='cdadmap.SurveyPanel', to_field=b'Organization_Name', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locationpanel',
            name='Organization_Name',
            field=models.ForeignKey(to='cdadmap.SurveyPanel', to_field=b'Organization_Name', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meetingpanel',
            name='Organization_Name',
            field=models.ForeignKey(to='cdadmap.SurveyPanel', to_field=b'Organization_Name', null=True),
            preserve_default=True,
        ),
    ]
