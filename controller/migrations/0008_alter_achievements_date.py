# Generated by Django 5.0.7 on 2024-07-20 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0007_alter_achievements_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievements',
            name='date',
            field=models.DateField(),
        ),
    ]
