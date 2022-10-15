# Generated by Django 4.1.1 on 2022-10-14 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_article_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.users', to_field='username'),
        ),
        migrations.AlterField(
            model_name='article',
            name='categorys',
            field=models.ManyToManyField(db_table='db_article2category', related_name='category_list', to='api.category'),
        ),
    ]