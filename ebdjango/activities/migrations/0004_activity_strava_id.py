# Generated by Django 2.1.5 on 2020-11-21 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_activity_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='strava_id',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
