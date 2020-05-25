# Generated by Django 2.2.4 on 2020-05-23 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faceapp', '0015_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faceapp.ClassRoom')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faceapp.Subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faceapp.Teacher')),
            ],
        ),
    ]