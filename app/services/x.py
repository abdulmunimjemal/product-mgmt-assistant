import tweepy
from core.config import settings
from datetime import datetime, timedelta
import re


X_BEARER_TOKEN = settings.X_BEARER_TOKEN

client = tweepy.Client(bearer_token=X_BEARER_TOKEN, wait_on_rate_limit=False)

def fetch_tweets(product: str, time_period: str, max_tweets: int = 10):
    """
    Fetch tweets matching the product query from within a given time period.
    
    Parameters:
        product (str): The search query.
        time_period (str): Time period string like '1d', '30m', '1h' etc.
        max_tweets (int): Maximum number of tweets to fetch.
    
    Returns:
        List[tweepy.Tweet]: Tweets sorted in descending order of retweet count.
    """
    # Parse the time period string (e.g., '1d', '30m', '1h')
    match = re.match(r"(\d+)([dhm])", time_period)
    if not match:
        raise ValueError("Invalid time period format. Use formats like '1d', '30m', '1h', etc.")
    value, unit = match.groups()
    value = int(value)
    
    # Determine the appropriate timedelta based on unit
    if unit == "d":
        delta = timedelta(days=value)
    elif unit == "h":
        delta = timedelta(hours=value)
    elif unit == "m":
        delta = timedelta(minutes=value)
    else:
        return {"success": False, "error": "Unsupported time period unit " + unit + ". Use 'd', 'h', or 'm'."}
        
    # Calculate the start time (UTC) for the search query
    now = datetime.utcnow()
    start_time = now - delta
    start_time_str = start_time.isoformat("T") + "Z"  # Twitter expects ISO 8601 format
    
    # Perform the tweet search; note that in Twitter API v2, use query and start_time parameters.
    try:
        tweets_response = client.search_recent_tweets(
            query=product,
            start_time=start_time_str,
            max_results=max_tweets,
            sort_order="relevancy",
            tweet_fields=["public_metrics", "created_at", "lang", "source"]
        )
    except Exception as e:
        return {"success": False, "error": str(e)}
    
    # If no tweets are found, return an empty list.
    if tweets_response.data is None:
        return []
    
    tweets = tweets_response.data

    formatted_tweets = []
    for tweet in tweets:
        formatted_tweets.append(
            {
                "text": tweet.text,
                "retweets": tweet.public_metrics.get('retweet_count', 'NaN'),
                "replies": tweet.public_metrics.get('reply_count', 'NaN'),
                "likes": tweet.public_metrics.get('like_count', 'NaN'),
                "created_at": tweet.created_at,
                "lang": tweet.lang
            }
        )
    
    return formatted_tweets
