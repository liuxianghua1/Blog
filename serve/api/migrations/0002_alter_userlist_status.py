# Generated by Django 4.1.1 on 2022-10-07 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlist',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '禁用'), (1, '激活')], default=1),
        ),
    ]
