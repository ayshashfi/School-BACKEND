# Generated by Django 5.1 on 2024-08-28 19:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_remove_leaveapplication_user_and_more'),
        ('main', '0010_alter_student_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveapplication',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student'),
        ),
    ]
