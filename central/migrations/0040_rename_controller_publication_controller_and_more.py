# Generated by Django 5.0.7 on 2024-07-21 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0039_remove_awards_staffs_awards_staffs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publication',
            old_name='Controller',
            new_name='controller',
        ),
        migrations.AddField(
            model_name='awards',
            name='controller',
            field=models.BooleanField(default=False, null=True, verbose_name='Controller Approval Status'),
        ),
        migrations.AddField(
            model_name='awards',
            name='hodapproval',
            field=models.BooleanField(default=False, null=True, verbose_name='HoD Approval Status'),
        ),
        migrations.AddField(
            model_name='phd',
            name='controller',
            field=models.BooleanField(default=False, null=True, verbose_name='Controller Approval Status'),
        ),
        migrations.AddField(
            model_name='phd',
            name='hodapproval',
            field=models.BooleanField(default=False, null=True, verbose_name='HoD Approval Status'),
        ),
        migrations.AddField(
            model_name='r2',
            name='controller',
            field=models.BooleanField(default=False, null=True, verbose_name='Controller Approval Status'),
        ),
        migrations.AddField(
            model_name='r2',
            name='hodapproval',
            field=models.BooleanField(default=False, null=True, verbose_name='HoD Approval Status'),
        ),
        migrations.AddField(
            model_name='r3',
            name='controller',
            field=models.BooleanField(default=False, null=True, verbose_name='Controller Approval Status'),
        ),
        migrations.AddField(
            model_name='r3',
            name='hodapproval',
            field=models.BooleanField(default=False, null=True, verbose_name='HoD Approval Status'),
        ),
    ]
