# Generated by Django 5.1 on 2024-08-28 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0001_initial'),
        ('main', '0010_alter_student_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaveapplication',
            name='user',
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.student'),
        ),
    ]
