# Generated by Django 5.0.7 on 2024-07-21 06:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_department_hod'),
        ('controller', '0012_achievements_staff_achievements_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='achievements',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.department'),
        ),
        migrations.RemoveField(
            model_name='achievements',
            name='staff',
        ),
        migrations.AddField(
            model_name='achievements',
            name='staff',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
