from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
import requests
from .models import Movie, Twitter
from .forms import SignUpForm
from math import ceil
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models
# for twitter analysis
import csv, tweepy, re
from textblob import TextBlob
from .function import *


# Create your views here.
def home(request):

    response = requests.get('https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm')
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find('tbody', {'class': 'lister-list'}).find_all('tr')
    final_postings = []
    i = 0
    for post in post_listings:
        post_titile = post.find('td', {'class': 'titleColumn'}).find('a').text

        if post.find('td', {'class': 'ratingColumn imdbRating'}).find('strong'):
            post_rating = post.find('td', {'class': 'ratingColumn imdbRating'}).find('strong').text
            post_rating = float(post_rating)
            post_rating_percent = post_rating * 7
        else:
            post_rating = "N/A"
            post_rating_percent = 0

        post_poster_filter = post.find('td', {'class': 'posterColumn'}).find('img').get('src').split('UY67')[0]
        if "UX45" in post_poster_filter:
            post_poster_filter = post.find('td', {'class': 'posterColumn'}).find('img').get('src').split('UX45')[0]

        post_poster = post_poster_filter + "UY450_AL_.jpg"


        if i < 50:
            final_postings.append((post_titile, post_rating, post_poster, post_rating_percent))

        i = i + 1

    # rotten tomato


    stuff_for_frontend = {
        'final_postings': final_postings,
    }

    return render(request, 'main/index.html', stuff_for_frontend)



def userRegister(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'main/userRegister.html', {'form': form})


def movieDetail(request, pk=None):
    if pk:
        obj = Movie.objects.get(id=pk)
    else:
        obj = Movie.objects.get(id=1)
    # get total twitter post
    objTwitter = Twitter.objects.get(id=1)
    totalTweet = int(objTwitter.total_tweet)
    # create authentication for accessing Twitter
    consumer_key = 'mnEweqTuvfyYoxWPWcHIvzMKe'
    consumer_secret = 'CgSmSiYpR4mIu15QahhWUGLLnGUPOjmHlPJhYdjbFOKDAZTEBi'
    access_token = '1222085686087438341-jevnePwSMmruYlZ0WmVsUzg7JGnw0Q'
    access_token_secret = 'eIrqApYh5LhitG8K2HQRvTEr7MCYt1Se1TFEE4tiMorya'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # initialize Tweepy API
    api = tweepy.API(auth)
    hashtag_phrase = obj.movie_title + "movie"
    # get the name of the spreadsheet we will write to
    fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))

    positive = 0
    negative = 0
    neutral = 0
    # open the spreadsheet we will write to
    with open('./movieDataset.csv', 'w', newline='') as file:
        w = csv.writer(file)

        # write header row to spreadsheet
        w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count'])

        # for each tweet matching our hashtags, write relevant info to the spreadsheet
        positiveTweet = []
        negativeTweet = []
        for tweet in tweepy.Cursor(api.search, q=hashtag_phrase + ' -filter:retweets', \
                                   lang="en", tweet_mode='extended').items(totalTweet):
            # remove some unneccesary word in text
            clean_text = cleanTxt(tweet.full_text)
            # tokenize and remove stopwords
            clean_text = textProcessing(clean_text)
            # sentiment analysis
            analysis = TextBlob(clean_text)
            i = j = 0
            if analysis.sentiment.polarity == 0:  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif 0 < analysis.sentiment.polarity <= 1:
                if analysis.sentiment.polarity >= 0.5:
                    if i < 3:
                        positiveTweet.append(tweet.full_text)
                        i = i + 1
                # print('positive' + str(analysis.sentiment.polarity))

                positive += 1
            else:
                if analysis.sentiment.polarity <= -0.3:
                    if j < 3:
                        negativeTweet.append(tweet.full_text)
                        j = j + 1
                # print('negative' + str(analysis.sentiment.polarity))

                negative += 1


            # textProcessing(clean_text)
            '''
            w.writerow([tweet.created_at, clean_text.replace('\n', ' ').encode('utf-8'),
                        tweet.user.screen_name.encode('utf-8'),
                        [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])'''
        sum = positive / (positive + negative) * 100
        sum = round(sum, 2)
    context = {
        'title': obj.movie_title,
        'description': obj.movie_desc,
        'image': obj.movie_image_url,
        'youtube': obj.movie_imdb_url,
        'adventure' : obj.movie_adventure,
        'action': obj.movie_action,
        'animation': obj.movie_animation,
        'horror': obj.movie_horror,
        'imdb': obj.movie_rating,
        'rating': sum,
        'commentpositive': positiveTweet,
        'commentnegative': negativeTweet,
    }
    return render(request, 'main/movieDetail.html', context)


def resultSearch(request):
    try:
        search = request.GET.get('search')
    except:
        search = 'none'
    movies = Movie.objects.filter(movie_title__icontains=search)

    context = {
        'query': search,
        'movies': movies
    }
    return render(request, 'main/resultSearch.html', context)

def movieUpdate(request):
    if request.method == 'POST':
        try:
            link = request.POST.get('movieLink')
            response = requests.get(link)
            data = response.text
            soup = BeautifulSoup(data, features='html.parser')
            post = soup.find('body')
            title = post.find('h1').contents[0]
            year = post.find('span', {'id': 'titleYear'}).find('a').contents[0]
            summary = post.find('div', {'class': 'summary_text'}).text
            summary = re.sub('\s\s+', ' ', summary)
            genre = post.find('div', {'class': 'subtext'}).select("a[href*=genres]")
            genre = [g.contents[0] for g in genre]

            image = post.find('div', {'class': 'poster'}).find('img').get('src').split('UX182')[0]
            image = image + "UY450_AL_.jpg"
            release_date = post.find('div', {'class': 'subtext'}).find('a', href=re.compile("release")).contents[0]
            video_url = post.find('div', {'class': 'slate'}).find('a').get('data-video')
            video_url = "https://www.imdb.com/video/imdb/" + video_url + "/imdb/embed?autoplay=false&width=640"
            if post.find('div', {'class': 'ratingValue'}):
                rating = post.find('div', {'class': 'ratingValue'}).find('span', {'itemprop': 'ratingValue'}).text
            else:
                rating = 'N/A'

            movie = Movie()
            movie.movie_title = title
            movie.movie_desc = summary
            movie.movie_year = year
            movie.movie_image_url = image
            movie.movie_release_date = release_date
            movie.movie_imdb_url = video_url
            movie.movie_rating = rating
            if "Action" in genre:
                movie.movie_action = True
            if "Adventure" in genre:
                movie.movie_adventure = True
            if "Animation" in genre:
                movie.movie_animation = True
            if "Horror" in genre:
                movie.movie_horror = True
            movie.save()
            success = "Yes"
        except:
            success = 'No'
    context ={
        'success': success,
    }
    return render(request, 'main/updateMovie.html', context)

def movieList(request):

    movies = Movie.objects.filter(movie_action=True)


    context = {
        'movies': movies
    }
    return render(request, 'main/movieList.html', context)