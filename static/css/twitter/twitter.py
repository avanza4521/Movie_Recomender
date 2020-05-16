import json
import csv
import tweepy
import re
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
import nltk

def percentage(part, whole):
    return 100 * float(part)/ float(whole)

def cleanTxt(text):
    text = text.lower()  # lowercase
    text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
    text = re.sub(r'\b\d+(?:\.\d+)?\s+', '', text)  # removing punctuation
    text = ''.join(c for c in text if not c.isdigit())  # removing number
    text = re.sub('#', '', text)  # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text)  # Removing RT
    text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
    text = text.strip()

    # removing foreigb language
    words = set(nltk.corpus.words.words())
    text = " ".join(w for w in nltk.wordpunct_tokenize(text) \
                    if w.lower() in words or not w.isalpha())
    return text

def textProcessing(text):
    # tokenize the text
    t = TextBlob(text)
    tokenizer = RegexpTokenizer(r'\w+')
    token = tokenizer.tokenize(text)

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in token if not w in stop_words]
    for w in token:
        if w not in stop_words:
            filtered_sentence.append(w)
    combine = TreebankWordDetokenizer().detokenize(filtered_sentence)

    # print(combine)
    return combine




# create authentication for accessing Twitter
consumer_key = 'mnEweqTuvfyYoxWPWcHIvzMKe'
consumer_secret = 'CgSmSiYpR4mIu15QahhWUGLLnGUPOjmHlPJhYdjbFOKDAZTEBi'
access_token = '1222085686087438341-jevnePwSMmruYlZ0WmVsUzg7JGnw0Q'
access_token_secret = 'eIrqApYh5LhitG8K2HQRvTEr7MCYt1Se1TFEE4tiMorya'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

    # initialize Tweepy API
api = tweepy.API(auth)
hashtag_phrase = input('Hashtag Phrase: ')
    # get the name of the spreadsheet we will write to
fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))

    # open the spreadsheet we will write to
with open('./movieDataset.csv', 'w', newline='', encoding='utf-8') as file:
    w = csv.writer(file)

        # write header row to spreadsheet
    w.writerow(['timestamp', 'clean_tweet_text', 'username', 'all_hashtags', 'followers_count'])

    positive = 0
    negative = 0
    neutral = 0
    # for each tweet matching our hashtags, write relevant info to the spreadsheet
    for tweet in tweepy.Cursor(api.search, q=hashtag_phrase + ' -filter:retweets', \
                                   lang="en", tweet_mode='extended').items(50):
        clean_text = cleanTxt(tweet.full_text)
        filterClean = textProcessing(clean_text)
        print("Clean :" + filterClean)
        print("NoClean :" + tweet.full_text)
        w.writerow([tweet.created_at, filterClean, tweet.user.screen_name.encode('utf-8'),
                        [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])



