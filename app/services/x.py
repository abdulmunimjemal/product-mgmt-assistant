import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

X_CONSUMER_KEY = os.getenv("X_CONSUMER_KEY")
X_CONSUMER_SECRET = os.getenv("X_CONSUMER_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

if not X_CONSUMER_KEY or not X_CONSUMER_SECRET or not X_ACCESS_TOKEN or not X_ACCESS_TOKEN_SECRET:
    raise ValueError("Missing Twitter API keys")


auth = tweepy.OAuth1UserHandler(
    X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

try:
    assert api.verify_credentials().screen_name != None
except:
    raise ValueError("Invalid Twitter API keys")

def fetch_tweets(product: str, max_tweets: int):
    tweets = api.search(
        q=product,
        count=max_tweets,
        result_type="recent",
        tweet_mode="extended",
        lang="en",
    )