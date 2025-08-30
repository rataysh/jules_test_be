import asyncio
import os
from datetime import datetime, timedelta
from twikit import Client
from app.core.config import settings

async def get_tweets_from_links(twitter_links: list[str], days: int) -> list[str]:
    """
    Fetches recent tweets from a list of Twitter profile URLs.

    Args:
        twitter_links: A list of URLs to Twitter profiles.
        days: The number of days back to search for tweets.

    Returns:
        A list of tweet contents as strings.
    """
    if not os.path.exists(settings.TWITTER_COOKIES_FILE):
        print(f"Error: Twitter cookies file not found at {settings.TWITTER_COOKIES_FILE}")
        return ["Error: Twitter cookies file not found. Please configure it in .env."]

    client = Client('en-US')
    try:
        await client.login_with_cookies(settings.TWITTER_COOKIES_FILE)
    except Exception as e:
        print(f"Error logging into Twitter: {e}")
        return [f"Error: Could not log into Twitter using cookies. Please check the file. Details: {e}"]

    all_tweets = []
    since_date = datetime.now() - timedelta(days=days)

    for link in twitter_links:
        username = link.split('/')[-1]
        if not username:
            continue

        try:
            user = await client.get_user_by_screen_name(username)
            if not user:
                continue

            tweets = await user.get_tweets('Tweets', count=40) # Get recent tweets

            for tweet in tweets:
                if tweet.created_at >= since_date:
                    all_tweets.append(f"Post from {user.name} (@{username}): {tweet.text}")

        except Exception as e:
            print(f"Error fetching tweets for {username}: {e}")
            # Continue to the next user even if one fails
            continue

    return all_tweets
