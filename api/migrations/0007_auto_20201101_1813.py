# Generated by Django 2.0.6 on 2020-11-01 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20201101_1658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='User_name',
            new_name='user_name',
        ),
    ]