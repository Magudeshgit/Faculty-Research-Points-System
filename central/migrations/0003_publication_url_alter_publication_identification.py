# Generated by Django 5.0.7 on 2024-07-14 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0002_publication_controller_publication_hodapproval'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='url',
            field=models.CharField(max_length=50, null=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='identification',
            field=models.CharField(max_length=25, verbose_name='ISSN/DOI No'),
        ),
    ]
