# Generated by Django 2.2.7 on 2020-06-18 02:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0014_auto_20200610_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='partNames',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), null=True, size=None),
        ),
    ]
