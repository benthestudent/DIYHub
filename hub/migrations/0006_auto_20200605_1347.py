# Generated by Django 2.2.7 on 2020-06-05 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0005_auto_20200605_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='firstn',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='lastn',
            field=models.CharField(max_length=20, null=True),
        ),
    ]