# Generated by Django 3.0.2 on 2020-03-09 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_auto_20200309_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie_year',
            field=models.CharField(max_length=10),
        ),
    ]