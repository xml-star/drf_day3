# Generated by Django 2.0.6 on 2020-11-01 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Users',
        ),
    ]