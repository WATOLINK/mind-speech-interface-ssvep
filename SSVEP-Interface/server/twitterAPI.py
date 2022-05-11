import tweepy
import os
from dotenv import load_dotenv

tweeting = False

def tweet(data):
    load_dotenv()

    BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
    CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
    CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
    ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")    

    api = tweepy.Client(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api.create_tweet(text=data)

def isTweeting():
    return tweeting

if __name__ == "__main__":
    tweet("L + ratio")