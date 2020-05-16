import re
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
import nltk


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

def cleanTxt(text):
    text = text.lower()  # lowercase
    text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
    text = re.sub(r'\b\d+(?:\.\d+)?\s+', '', text)  # removing punctuation
    text = ''.join(c for c in text if not c.isdigit())  # removing number
    text = re.sub('#', '', text)  # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text)  # Removing RT
    text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
    text = text.strip()

    # removing non alphabet language
    words = set(nltk.corpus.words.words())
    text = " ".join(w for w in nltk.wordpunct_tokenize(text) \
                    if w.lower() in words or not w.isalpha())
    return text


