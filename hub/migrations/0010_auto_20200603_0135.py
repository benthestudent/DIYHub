# Generated by Django 2.2.7 on 2020-06-03 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0009_comment_commentparent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='project',
            field=models.ManyToManyField(blank=True, to='hub.Project'),
        ),
    ]
