# Generated by Django 5.0.7 on 2024-07-22 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0040_rename_controller_publication_controller_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ipr',
            old_name='Controller',
            new_name='controller',
        ),
    ]
