# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0004_auto_20141216_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationpanel',
            name='Organization_Name',
            field=models.TextField(),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='locationpanel',
            name='idlocation',
            field=models.ForeignKey(primary_key=True, serialize=False, to='cdadmap.SurveyPanel'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meetingpanel',
            name='Organization_Name',
            field=models.TextField(),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meetingpanel',
            name='id',
            field=models.ForeignKey(primary_key=True, serialize=False, to='cdadmap.SurveyPanel'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpanel',
            name='Organization_Name',
            field=models.TextField(),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contactpanel',
            name='id',
            field=models.ForeignKey(primary_key=True, serialize=False, to='cdadmap.SurveyPanel'),
            preserve_default=True,
        ),
    ]
