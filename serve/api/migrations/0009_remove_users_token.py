# Generated by Django 4.1.1 on 2022-10-13 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_users_options_alter_users_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='token',
        ),
    ]
