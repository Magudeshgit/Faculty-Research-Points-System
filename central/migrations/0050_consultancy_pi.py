# Generated by Django 5.0.7 on 2024-07-25 10:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0049_remove_publication_issn_alter_publication_doi_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='consultancy',
            name='pi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pi', to=settings.AUTH_USER_MODEL),
        ),
    ]
