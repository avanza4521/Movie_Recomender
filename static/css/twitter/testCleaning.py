import string
import re
from textblob import TextBlob
from nltk.corpus import stopwords


# 1. meke text all lower case
# 2. remove puntuation
# 3. Remove numerical values
# 4. Remove common non-sensical text (/n)
# 5. Tokenize text
# 6. Remove stop words
text = ["b'idk if it\xe2\x80\x99s just me , maybe i\xe2\x80\x99m trippin but has sonic stuff been tasting different lately ? like the blasts and drinks ? bc to me it taste like burnt or machine .. i\xe2\x80\x99m like 99.9% positive somethin is different . but ppl are telling me it taste fine ..'"]
textObject = TextBlob(text)

documentsentence = textObject.words

raw_docs = ["Here are some very simple basic sentences.",
"They won't be very interesting, I'm afraid.",
"The point of these examples is to _learn how basic text cleaning works_ on *very simple* data."]


# Tokenizing text into bags of words
from nltk.tokenize import word_tokenize
tokenized_docs = [word_tokenize(doc) for doc in raw_docs]
print(tokenized_docs)

regex = re.compile(
    '[%s]' % re.escape(string.punctuation))  # see documentation here: http://docs.python.org/2/library/string.html

tokenized_docs_no_punctuation = []

for review in tokenized_docs:
    new_review = []
    for token in review:
        new_token = regex.sub(u'', token)
        if not new_token == u'':
            new_review.append(new_token)

    tokenized_docs_no_punctuation.append(new_review)

print(tokenized_docs_no_punctuation)

# Cleaning text of stopwords
from nltk.corpus import stopwords

tokenized_docs_no_stopwords = []

for doc in tokenized_docs_no_punctuation:
    new_term_vector = []
    for word in doc:
        if not word in stopwords.words('english'):
            new_term_vector.append(word)

    tokenized_docs_no_stopwords.append(new_term_vector)

print(tokenized_docs_no_stopwords)

# Stemming and Lemmatizing
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

porter = PorterStemmer()
snowball = SnowballStemmer('english')
wordnet = WordNetLemmatizer()

preprocessed_docs = []

for doc in tokenized_docs_no_stopwords:
    final_doc = []
    for word in doc:
        final_doc.append(porter.stem(word))
        # final_doc.append(snowball.stem(word))
        # final_doc.append(wordnet.lemmatize(word))

    preprocessed_docs.append(final_doc)

print(preprocessed_docs)

'''
# convert to lower case
text = text.lower()
print('1.' + text)

# remove punctuation and numbers
text = re.sub('\[.*?\]', '', text)
text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
text = re.sub('\w*\d\w*', '', text)
print('2/3. ' + text)
'''
''''
text = re.sub('[‘’“”…]', '', text)
text = re.sub('\n', '', text)
print('4. ' + text)

from nltk.corpus import stopwords

stop_words = stopwords.words('english')
print(len(stop_words))'''