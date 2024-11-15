# Generated by Django 5.0.6 on 2024-07-13 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empid', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveApl',
            fields=[
                ('aplid', models.AutoField(primary_key=True, serialize=False)),
                ('apl_date', models.DateField(auto_now_add=True)),
                ('leaveDate', models.DateField()),
                ('returnDate', models.DateField()),
                ('reason', models.CharField(choices=[('PER', 'Personal Leave'), ('OFI', 'Official Work'), ('PTO', 'Paid Time Off'), ('EMR', 'Emergency')], max_length=3)),
                ('status', models.CharField(choices=[('SUB', 'Submitted'), ('ACP', 'Accepted'), ('REJ', 'Rejected'), ('DEF', 'Deffered')], max_length=3)),
                ('empid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMSApp.employee')),
            ],
        ),
    ]
