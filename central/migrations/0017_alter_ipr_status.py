# Generated by Django 5.0.7 on 2024-07-17 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0016_alter_ipr_options_ipr_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipr',
            name='status',
            field=models.CharField(choices=[('filing', 'filing'), ('granted', 'granted')], max_length=50, null=True),
        ),
    ]
