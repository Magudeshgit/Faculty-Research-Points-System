# Generated by Django 5.0.7 on 2024-07-26 11:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0050_consultancy_pi'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultancy',
            name='pi',
        ),
        migrations.AddField(
            model_name='funding',
            name='pi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pi', to=settings.AUTH_USER_MODEL),
        ),
    ]
