# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0027_surveypanel_cdad_services_other'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveypanel',
            name='CDAD_Services_Other',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
