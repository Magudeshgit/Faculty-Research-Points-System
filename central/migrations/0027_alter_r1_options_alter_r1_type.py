# Generated by Django 5.0.7 on 2024-07-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0026_r1'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='r1',
            options={'verbose_name': 'Research Related Attending', 'verbose_name_plural': 'Research Related Attendings'},
        ),
        migrations.AlterField(
            model_name='r1',
            name='type',
            field=models.CharField(choices=[('STTP', 'STTP'), ('FDP (NPTEL excluded)', 'FDP'), ('Seminar', 'Seminar'), ('Workshop', 'Workshop')], max_length=25),
        ),
    ]
