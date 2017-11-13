import praw
import datetime as dt
import time
import os
import pandas as pd
import numpy as np
import pickle
from pymongo import MongoClient

# Connect to Reddit API
REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']

REDDIT_U = os.environ["REDDIT_U"]
REDDIT_P = os.environ["REDDIT_P"]
REDDIT_USER_AGENT = os.environ["REDDIT_USER_AGENT"]

reddit = praw.Reddit(client_id = REDDIT_CLIENT_ID,
                    client_secret = REDDIT_CLIENT_SECRET,
                    username = REDDIT_U,
                    password = REDDIT_P,
                    user_agent = REDDIT_USER_AGENT)


def get_all_comments(r, submission_id):
    """
    Gets all parent comments from a reddit submission.

    :param r: PRAW object
    :param submission_id: id of the submission
    :returns: list of comments from that submission
    """

    submission = r.submission(submission_id)
    submission.comments.replace_more(limit=0)
    comments_list = []
    for comment in submission.comments.list():
        comment_age = (submission.created - comment.created)* -1
        comments_list.append((comment.body, comment.score, comment_age / 60))
    return comments_list


# Connect to MongoDB
MONGO_U = os.environ["MONGO_REDDIT_COMMENTS_DB_U"]
MONGO_P = os.environ["MONGO_REDDIT_COMMENTS_DB_P"] 

client = MongoClient('mongodb://' + MONGO_U + ':' + MONGO_P + '@localhost:27017/reddit_comments_db')
db = client['reddit_comments_db']

today = dt.datetime.now().date()
subreddits = ['politics', 'atheism', 'hiphopheads', 'science', 'worldnews']

for sub_name in subreddits:
    subreddit = reddit.subreddit(sub_name)
    posts = subreddit.top(limit=100, time_filter='year')

    collection = db['{}_comments_collection'.format(sub_name)]

    for post in posts:
        print('Getting comments for {0} {1}'.format(sub_name, post))
        date_created = dt.datetime.fromtimestamp(post.created).date()
        post_age = (today - date_created).days
        comments = get_all_comments(reddit, post)

        data = {}

        data['comments'] = comments
        data['post_age'] = post_age
        data['post_id'] = post.id
        data['subreddit'] = sub_name

        pickle_name = '{0}_{1}_comments.pickle'.format(sub_name, post)

        with open(pickle_name, 'wb') as f:
            pickle.dump(data, f)

        collection.insert_one(data)
        print('Inserted into DB')

print('COMPLETE')
