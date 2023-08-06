# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 23:53:32 2020

@author: Ankit Raj
"""
import re
import numpy as np
import pandas as pd
import multiprocessing as mp
import nltk
nltk.download('brown')
nltk.download('name')
from nltk.tokenize import regexp_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob
import string
from collections import Counter
from sklearn.base import TransformerMixin, BaseEstimator
from normalise import normalise

class TextSlack(BaseEstimator, TransformerMixin):
    def __init__(self, multicore=False, stop_words=stopwords.words('english'), lemmatizer=WordNetLemmatizer()):
        self.multicore = multicore
        self.stop_words = stop_words
        self.lemmatizer = lemmatizer

    def fit(self, X, y=None):
        return self

    def transform(self, X, *_):
        if type(X) != pd.core.frame.DataFrame:
            return self.preprocess_text(X)
        else:
            X_copy = X.copy()
        cores = mp.cpu_count()
        if self.multicore == True:
            n_jobs = cores
        else:
            return X_copy.apply(self._preprocess_text(X_copy))
        data_split = np.array(X, n_jobs)
        pool = mp.Pool(cores)
        processed_data = pd.concat(pool.map(self._preprocess_data_split, data_split))
        return processed_data
    
    def _preprocess_data_split(self, data_split):
        return data_split.apply(self.preprocess_text)

    def preprocess_text(self, text):
        normalized_text = self._normalize(text.lower())
        normalized_text = re.sub(' +', ' ', normalized_text)
        words = regexp_tokenize(text.lower(), r'[A-Za-z]+')
        removed_punct = self._remove_punct(words)
        removed_stopwords = self._remove_stopwords(removed_punct)
        return self._lemmatize(removed_stopwords)

    def _normalize(self, text):
        try:
            return ' '.join(normalise(text, verbose=False))
        except:
            return text

    def _remove_punct(self, words):
        return [w for w in words if w not in string.punctuation]

    def _remove_stopwords(self, words):
        return [w for w in words if w not in self.stop_words]

    def _lemmatize(self, words):
        return ' '.join([self.lemmatizer.lemmatize(w) for w in words])
    
    def extract_nouns(self, text):
        processed_text = self._preprocess_text(text)
        pos_tags, _ = self._blob_features(processed_text)
        return ' '.join([w for w, p in pos_tags if p == 'NN'])
    
    def extract_verbs(self, text):
        processed_text = self.preprocess_text(text)
        pos_tags, _ = self._blob_features(processed_text)
        return ' '.join([w for w, p in pos_tags if p == 'VB'])
      
    def extract_adjectives(self, text):
        processed_text = self.preprocess_text(text)
        pos_tags, _ = self._blob_features(processed_text)
        return ' '.join([w for w, p in pos_tags if p == 'JJ'])
    
    def extract_adverbs(self, text):
        processed_text = self.preprocess_text(text)
        pos_tags, _ = self._blob_features(processed_text)
        return ' '.join([w for w, p in pos_tags if p == 'RB'])
    
    def sentiment(self, text):
        processed_text = self.preprocess_text(text)
        _, polarity = self._blob_features(processed_text)
        return 'pos' if polarity > 0.0 else 'neg' if polarity < 0.0 else 'neu'

    def _blob_features(self, text):
        blob = TextBlob(text)
        return blob.tags, blob.polarity
    
    def word_occurances(self, word, text):
        word_count_dic = dict(Counter([w for w in text.split()]))
        return [c for w, c in word_count_dic.items() if w==word][0]
    