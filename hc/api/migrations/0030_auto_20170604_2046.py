# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-04 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20170604_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='alert_after',
            field=models.DurationField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='check',
            name='last_nag_alert',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
