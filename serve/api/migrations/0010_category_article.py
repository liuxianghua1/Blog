# Generated by Django 4.1.1 on 2022-10-14 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_users_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('clicks', models.IntegerField(default=0)),
                ('status', models.SmallIntegerField(choices=[(0, '隐藏'), (1, '展示')], default=1)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.users', to_field='username')),
                ('categorys', models.ManyToManyField(db_table='db_article2category', to='api.category')),
            ],
        ),
    ]