# Generated by Django 5.0.7 on 2024-08-03 09:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_staff_dept'),
        ('controller', '0017_rewardpoints_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='rewardpoints',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.department'),
        ),
    ]
