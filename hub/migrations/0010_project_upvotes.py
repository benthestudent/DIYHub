# Generated by Django 2.2.7 on 2020-06-08 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0009_remove_comment_upvotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
