import pytest
import json
from unittest.mock import patch, AsyncMock
from app.services.openai_service import get_news_from_openai
from app.api.schemas import NewsRequest

# Reusable mock for the OpenAI API response
class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockMessage:
    def __init__(self, content):
        self.content = content

@pytest.mark.asyncio
@patch("app.services.openai_service.get_tweets_from_links", new_callable=AsyncMock)
@patch("app.services.openai_service.client.chat.completions.create", new_callable=AsyncMock)
async def test_get_news_from_openai_success(mock_openai_create, mock_get_tweets):
    """
    Test the success path of get_news_from_openai.
    Ensures it calls dependencies and returns a valid summary.
    """
    # Arrange: Mock dependencies
    mock_get_tweets.return_value = ["A tweet about AI."]
    mock_summary = {"official_news": [{"company": "Test", "updates": []}]}
    mock_choice = MockChoice(json.dumps(mock_summary))
    mock_openai_create.return_value = type("MockResponse", (), {"choices": [mock_choice]})()

    request = NewsRequest(twitter_links=["http://twitter.com/test"], days=1, language="en")

    # Act: Call the function
    result = await get_news_from_openai(request)

    # Assert: Check results and mock calls
    assert result == mock_summary
    mock_get_tweets.assert_called_once_with(["http://twitter.com/test"], 1)
    mock_openai_create.assert_called_once()

@pytest.mark.asyncio
@patch("app.services.openai_service.get_tweets_from_links", new_callable=AsyncMock)
@patch("app.services.openai_service.client.chat.completions.create", new_callable=AsyncMock)
async def test_get_news_from_openai_scraper_error(mock_openai_create, mock_get_tweets):
    """
    Test how get_news_from_openai handles an error from the Twitter scraper.
    It should return a structured error message and not call the OpenAI API.
    """
    # Arrange: Mock the scraper to return an error
    mock_get_tweets.return_value = ["Error: Scraper failed."]
    request = NewsRequest(twitter_links=[], days=1, language="en")

    # Act: Call the function
    result = await get_news_from_openai(request)

    # Assert: Check the error structure
    assert "error" in result
    assert result["error"] == "Error: Scraper failed."
    assert "Scraper failed" in result["rumors_and_hot_topics"][0]["theme"]
    mock_openai_create.assert_not_called()

@pytest.mark.asyncio
@patch("app.services.openai_service.get_tweets_from_links", new_callable=AsyncMock)
@patch("app.services.openai_service.client.chat.completions.create", new_callable=AsyncMock)
async def test_get_news_from_openai_no_tweets(mock_openai_create, mock_get_tweets):
    """
    Test how get_news_from_openai handles finding no tweets.
    It should return a message indicating no tweets were found and not call the OpenAI API.
    """
    # Arrange: Mock the scraper to return an empty list
    mock_get_tweets.return_value = []
    request = NewsRequest(twitter_links=[], days=1, language="en")

    # Act: Call the function
    result = await get_news_from_openai(request)

    # Assert: Check the response structure
    assert "error" in result
    assert result["error"] == "No tweets found."
    assert "No tweets found" in result["rumors_and_hot_topics"][0]["theme"]
    mock_openai_create.assert_not_called()
