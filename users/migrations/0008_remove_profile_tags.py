# Generated by Django 3.2.8 on 2021-10-19 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_profile_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='tags',
        ),
    ]
