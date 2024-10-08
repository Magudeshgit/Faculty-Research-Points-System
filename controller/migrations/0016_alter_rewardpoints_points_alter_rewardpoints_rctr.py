# Generated by Django 5.0.7 on 2024-07-25 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0015_rewardpoints_rctr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rewardpoints',
            name='points',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='rewardpoints',
            name='rctr',
            field=models.ManyToManyField(to='controller.criteria', verbose_name='Reward Criteria'),
        ),
    ]
