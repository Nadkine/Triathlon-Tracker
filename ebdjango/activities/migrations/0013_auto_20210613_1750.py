# Generated by Django 2.1.5 on 2021-06-13 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0012_auto_20210613_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(default=' ', max_length=50),
        ),
    ]