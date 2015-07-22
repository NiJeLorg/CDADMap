# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0024_auto_20150722_1305'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Parners',
            new_name='Partners',
        ),
        migrations.RenameField(
            model_name='partners',
            old_name='parnter_name',
            new_name='partner_name',
        ),
        migrations.RenameField(
            model_name='surveypanel',
            old_name='parners',
            new_name='partners',
        ),
    ]
