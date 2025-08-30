import json
from openai import AsyncOpenAI
from app.api.schemas import NewsRequest
from app.core.config import settings
from app.core.prompts import NEWS_AGGREGATOR_PROMPT

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def get_news_from_openai(request: NewsRequest) -> dict:
    """
    Generates a news summary by calling the OpenAI API.
    """
    twitter_links_str = "\n".join(request.twitter_links)

    prompt = NEWS_AGGREGATOR_PROMPT.format(
        twitter_links=twitter_links_str,
        days=request.days,
        language=request.language,
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-5-nano-2025-08-07",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # Handle potential API errors, e.g., authentication, rate limits
        print(f"An error occurred: {e}")
        return {"error": "Could not retrieve news summary."}
