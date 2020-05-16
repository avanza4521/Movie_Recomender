# Generated by Django 3.0.2 on 2020-04-20 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0007_movie_movie_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='movie_youtube_url',
            new_name='movie_imdb_url',
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_image_url',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_release_date',
            field=models.CharField(max_length=200, null=True),
        ),
    ]