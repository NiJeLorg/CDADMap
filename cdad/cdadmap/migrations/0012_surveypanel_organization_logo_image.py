# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0011_auto_20150624_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveypanel',
            name='Organization_Logo_Image',
            field=models.ImageField(null=True, upload_to=b'img/%Y_%m_%d_%h_%M_%s', blank=True),
            preserve_default=True,
        ),
    ]
