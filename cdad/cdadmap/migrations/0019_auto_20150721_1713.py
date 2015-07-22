# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0018_surveypanel_languages_other'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetingpanel',
            name='Occurances',
        ),
        migrations.RemoveField(
            model_name='meetingpanel',
            name='On1',
        ),
        migrations.RemoveField(
            model_name='meetingpanel',
            name='Repeat1',
        ),
        migrations.RemoveField(
            model_name='meetingpanel',
            name='RepeatEvery',
        ),
        migrations.RemoveField(
            model_name='meetingpanel',
            name='Time1',
        ),
        migrations.AddField(
            model_name='meetingpanel',
            name='all_day',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meetingpanel',
            name='end_repeat',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meetingpanel',
            name='repeat',
            field=models.CharField(default=b'NEVER', max_length=15, choices=[(b'NEVER', b'Never'), (b'DAILY', b'Every Day'), (b'WEEKDAY', b'Every Weekday'), (b'WEEKLY', b'Every Week'), (b'BIWEEKLY', b'Every 2 Weeks'), (b'MONTHLY', b'Every Month'), (b'YEARLY', b'Every Year')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meetingpanel',
            name='EndsOn',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meetingpanel',
            name='StartOn',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meetingpanel',
            name='hasMeeting',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
