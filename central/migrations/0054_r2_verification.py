# Generated by Django 5.0.7 on 2024-07-29 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0053_alter_awards_institutiontype_remove_r1_staffs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='r2',
            name='verification',
            field=models.BooleanField(null=True),
        ),
    ]
