from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
class Movie(models.Model):
    movie_title = models.CharField(max_length=200)
    movie_desc = models.CharField(max_length=500)
    movie_year = models.CharField(max_length=10, default='')
    movie_imdb_url = models.CharField(null=True, max_length=500)
    movie_image = models.FileField(null=True, blank=True)
    movie_image_url = models.CharField(null=True, max_length=500)
    movie_release_date = models.CharField(max_length=200, null=True)
    movie_rating = models.CharField(max_length=50, default='N/A')
    movie_adventure = models.BooleanField(default=False)
    movie_action = models.BooleanField(default=False)
    movie_animation = models.BooleanField(default=False)
    movie_horror = models.BooleanField(default=False)
    def __str__(self):
        return self.movie_title

class Twitter(models.Model):
    Edit_Tweet = 'Edit Tweet'
    total_tweet = models.CharField(max_length=50)
    def __str__(self):
        return self.Edit_Tweet




