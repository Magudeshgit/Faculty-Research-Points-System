# Generated by Django 5.0.7 on 2024-07-17 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0024_phd_department_alter_ipr_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phd',
            name='registerno',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='phd',
            name='type',
            field=models.CharField(choices=[('Guideship - ongoing', 'Guideship - ongoing'), ('Guideship - completed', 'Guideship - completed'), ('Ongoing Scholar', 'Ongoing Scholar'), ('Completed Scholar', 'Completed Scholar')], max_length=50),
        ),
    ]
