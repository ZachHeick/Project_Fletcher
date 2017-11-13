from pymongo import MongoClient
import pandas as pd
import numpy as np
import pickle
from sklearn.tree import DecisionTreeClassifier
import re
from nltk.corpus import stopwords
from nltk.stem import porter
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer

with open('../Data_Files/subreddits.pickle', 'rb') as f:
    subreddits = pickle.load(f)

with open('../Data_Files/models_d.pickle', 'rb') as f:
    models_d = pickle.load(f)


class RCC():
    """
    Wrapper class for dictionary of models.
    """
    def __init__(self, subreddit):
        self.model = models_d[subreddit]
        self.models_d = models_d
        self.subreddit = subreddit

        self.stopwords = stopwords.words()
        self.lemmatizer = WordNetLemmatizer()

    def get_subreddits(self):
        """
        Get available subreddits.
        :return: list of subreddit names
        """
        return self.models_d.keys()

    def __clean_comment(self, raw_comment):
        """
        Cleans individual comment by removing markdown and hyperlinks.
        :param raw_comment: uncleaned comment string
        :return: cleaned comment string
        """

        url_regex_markdown = "http[s]?://[^)]+"
        url_regex = "http\S+"

        comment_no_markdown = re.sub(r'\(\s*({})\s*\)'.format(url_regex_markdown), ' ', raw_comment) \
            .replace('*', '') \
            .replace('&nbsp;', '') \
            .replace('[', ' ').replace(']', ' ') \
            .replace('(', ' ').replace(')', ' ')
        cleaned_comment = re.sub(r'{}'.format(url_regex), ' ', comment_no_markdown, flags=re.MULTILINE) \
            .replace('\n', ' ')

        return cleaned_comment

    def __get_comment_data(self, raw_comment, time):
        """
        Gets comment metadata.
        :param raw_comment: comment
        :param time: time of comment made after submission was posted
        :return: dictionary of comment metadata
        """

        cleaned_comment = self.__clean_comment(raw_comment)

        comment_d = {}
        subjectivities = [0]
        polarities = [0]

        # Get comment subjectivity and polarity by sentence
        for split in re.split('[?:!.]', cleaned_comment):
            sentiment = TextBlob(split).sentiment
            if split != '':
                subjectivities.append(float('{0:.4f}'.format(sentiment.subjectivity)))
                polarities.append(float('{0:.4f}'.format(sentiment.polarity)))

        # More metadata
        sentiment = TextBlob(cleaned_comment).sentiment
        comment_d['max_subjectivity'] = max(subjectivities)
        comment_d['min_subjectivity'] = min(subjectivities)
        comment_d['max_polarity'] = max(polarities)
        comment_d['min_polarity'] = min(polarities)
        comment_d['overall_polarity'] = float('{0:.4f}'.format(sentiment.polarity))

        words = cleaned_comment.split()

        comment_d['words_count'] = len(words)
        comment_d['char_count'] = len(cleaned_comment.strip())
        comment_d['time'] = float('{0:.2f}'.format(time))

        # Lemmatizes words and removes stop words from comment
        cleaned_words = []
        for word in words:
            lemm_word = self.lemmatizer.lemmatize(word)
            if lemm_word not in self.stopwords:
                cleaned_words.append(lemm_word)
        comment_d['comment'] = ' '.join(cleaned_words)

        return comment_d

    def predict_comment(self, raw_comment, time):
        """
        Given a new comment, predict if a subreddit will like it.
        :param raw_comment: new comment
        :param time: time of comment after submission was posted
        :return: Prediction, either 0 or 1
        """
        comment_data = self.__get_comment_data(raw_comment, time)
        comment = comment_data['comment']

        tfidf = self.model[1]
        tfidf_train = self.model[2]
        df = pd.DataFrame(tfidf_train.toarray(), columns=tfidf.get_feature_names())

        comment_tfidf = TfidfVectorizer(ngram_range=(1, 3))
        comment_tfidf_fit = comment_tfidf.fit_transform([comment])
        comment_df = pd.DataFrame(columns=df.columns, dtype=float)
        comment_df.loc[0, :] = 0

        for word in comment_tfidf.get_feature_names():
            if word in comment_df.columns:
                comment_df[word] += 1

        other_features = [comment_data['char_count'],
                          comment_data['max_polarity'],
                          comment_data['max_subjectivity'],
                          comment_data['min_polarity'],
                          comment_data['min_subjectivity'],
                          comment_data['overall_polarity'],
                          comment_data['time'],
                          comment_data['words_count']
                          ]

        other_features_df = pd.DataFrame([other_features])
        predict_df = pd.concat([comment_df, other_features_df], axis=1)

        return int(self.model[0].predict(predict_df))



