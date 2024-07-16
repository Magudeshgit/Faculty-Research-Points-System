# Generated by Django 5.0.7 on 2024-07-16 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0007_consultancy_category_consultancy_receivedamount_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consultancy',
            options={'verbose_name': 'Consultancies and fundings', 'verbose_name_plural': 'Consultancies and fundings'},
        ),
        migrations.AlterField(
            model_name='consultancy',
            name='receivedamount',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='consultancy',
            name='sanctionedamount',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='consultancy',
            name='uc',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
