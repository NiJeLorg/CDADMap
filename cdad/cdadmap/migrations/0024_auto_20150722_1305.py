# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdadmap', '0023_auto_20150722_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parners',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parnter_name', models.CharField(default=b'', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='surveypanel',
            name='parners',
            field=models.ManyToManyField(to='cdadmap.Parners'),
            preserve_default=True,
        ),
    ]
