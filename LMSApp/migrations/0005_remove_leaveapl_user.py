# Generated by Django 5.0.6 on 2024-10-08 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LMSApp', '0004_employee_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaveapl',
            name='user',
        ),
    ]
