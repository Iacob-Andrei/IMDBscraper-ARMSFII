import nltk
import json
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def lemmatize_sentence(sentence):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(sentence)
    tagged_words = nltk.pos_tag(words)
    pos_dict = {'N': 'n', 'V': 'v', 'R': 'r', 'J': 'a'}
    
    lemmas = []
    for word, tag in tagged_words:
        if tag[0] in pos_dict:
            pos = pos_dict[tag[0]]
            lemma = lemmatizer.lemmatize(word, pos=pos)
        else:
            lemma = lemmatizer.lemmatize(word)
        lemmas.append(lemma)
    
    lemmas = [word for word in lemmas if word.isalpha()]
    lemmas = [word for word in lemmas if not word.lower() in stop_words]
    
    word_counts = {}
    for word in lemmas:
        if word not in word_counts:
            word_counts[word] = 1
        else:
            word_counts[word] += 1
    return word_counts


def process_movies(data):
    for index, item in enumerate(data): # parse every movie 
        for review in item['users_reviews']:    # parse every review
            text_to_analyze = review['title'] + '. ' + review['text']
            words = lemmatize_sentence(text_to_analyze)
            review['words'] = words

    with open("data/imdb_top_100_movies.json", "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)


def process_tvshows(data):
    for item in data:   # parse every series
        for season in item['seasons'].keys():       # parse every season
            for episode in item['seasons'][season]: # parse every episode
                for review in episode['reviews']:              # parse every review
                    text_to_analyze = review['title'] + '. ' + review['text']
                    words = lemmatize_sentence(text_to_analyze)
                    review['words'] = words
    
    with open("data/imdb_top_100_tv_series.json", "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)