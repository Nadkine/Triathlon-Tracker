# Generated by Django 2.1.5 on 2020-11-27 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0009_auto_20201127_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='user',
            field=models.CharField(default=' ', max_length=30),
        ),
    ]
