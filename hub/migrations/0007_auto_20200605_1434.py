# Generated by Django 2.2.7 on 2020-06-05 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0006_auto_20200605_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.BigIntegerField(null=True),
        ),
    ]
