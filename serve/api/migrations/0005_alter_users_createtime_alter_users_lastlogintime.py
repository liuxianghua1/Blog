# Generated by Django 4.1.1 on 2022-10-11 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_users_lastlogintime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='createtime',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='lastlogintime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
