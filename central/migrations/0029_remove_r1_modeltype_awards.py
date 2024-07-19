# Generated by Django 5.0.7 on 2024-07-18 17:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_department_hod'),
        ('central', '0028_alter_r1_options_r1_modeltype_alter_r1_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='r1',
            name='modeltype',
        ),
        migrations.CreateModel(
            name='awards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=100)),
                ('institutiontype', models.CharField(choices=[('from our Institution', 'from our Institution'), ('from top NIRF- ranked government and government-aided academic institutions, NPTEL Star performers/Topper certificate', 'from top NIRF- ranked government and government-aided academic institutions, NPTEL Star performers/Topper certificate'), ('from academic institutions in abroad/ Industry /Scientific bodies', 'from academic institutions in abroad/ Industry /Scientific bodies'), ('from Government Agencies-State/ National Awards', 'from Government Agencies-State/ National Awards')], max_length=150)),
                ('date', models.DateField()),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.department')),
                ('staffs', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
