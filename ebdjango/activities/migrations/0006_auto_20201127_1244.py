# Generated by Django 2.1.5 on 2020-11-27 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_activity_workout_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='workout_type',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
