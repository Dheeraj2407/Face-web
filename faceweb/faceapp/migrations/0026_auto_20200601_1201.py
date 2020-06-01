# Generated by Django 2.2.4 on 2020-06-01 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faceapp', '0025_auto_20200601_0608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancelogs',
            name='date',
        ),
        migrations.RemoveField(
            model_name='attendancelogs',
            name='time',
        ),
        migrations.AddField(
            model_name='attendancelogs',
            name='hour',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='teacherclass',
            name='last_class',
            field=models.IntegerField(default=0),
        ),
    ]
