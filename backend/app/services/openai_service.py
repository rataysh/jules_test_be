import json
from openai import AsyncOpenAI
from app.api.schemas import NewsRequest
from app.core.config import settings
from app.core.prompts import NEWS_AGGREGATOR_PROMPT
from app.services.twitter_service import get_tweets_from_links

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def get_news_from_openai(request: NewsRequest) -> dict:
    """
    Generates a news summary using a RAG approach:
    1. Fetches tweets using the twitter_service.
    2. Passes the tweet content to the OpenAI API for summarization.
    """
    # RAG Step 1: Retrieve data from Twitter
    tweet_context_list = await get_tweets_from_links(request.twitter_links, request.days)

    # Handle case where scraper fails
    if not tweet_context_list or "Error:" in tweet_context_list[0]:
        error_message = tweet_context_list[0] if tweet_context_list else "No tweets found."
        return {
            "official_news": [],
            "upcoming_announcements": [],
            "rumors_and_hot_topics": [{
                "theme": error_message,
                "sources": []
            }],
            "error": error_message
        }

    tweet_context_str = "\n\n".join(tweet_context_list)

    # RAG Step 2: Augment the prompt with the retrieved data
    prompt = NEWS_AGGREGATOR_PROMPT.format(
        tweet_context=tweet_context_str,
        language=request.language,
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo", # Using a more powerful model for better summarization
            messages=[
                {"role": "system", "content": "You are an expert AI news analyst. Your task is to summarize the provided text into a structured JSON format."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"An error occurred during OpenAI call: {e}")
        return {"error": f"Could not retrieve news summary from OpenAI. Details: {e}"}
