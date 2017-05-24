from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_current_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='daily_reports_allowed',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='weekly_reports_allowed',
            field=models.BooleanField(default=True),
        ),
    ]
