import pytest
import json
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock

from app.main import app
from app.api.schemas import NewsResponse

# Mock for the OpenAI API response structure
class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockMessage:
    def __init__(self, content):
        self.content = content

@pytest.mark.asyncio
@patch("app.services.openai_service.get_tweets_from_links", new_callable=AsyncMock)
@patch("app.services.openai_service.client.chat.completions.create", new_callable=AsyncMock)
async def test_generate_news_e2e_success(mock_openai_create, mock_get_tweets):
    """
    Test the /generate-news endpoint end-to-end with mocked external services.
    This test simulates the RAG flow:
    1. Mocks the Twitter service to return sample tweets.
    2. Mocks the OpenAI API to return a structured JSON summary.
    3. Asserts the final API response is correct.
    """
    # 1. Mock the Twitter service response
    mock_tweets_data = [
        "User @OpenAI: We just released a new model that can summarize text!",
        "User @TechCrunch: Rumors are swirling about a new AI chip from Google."
    ]
    mock_get_tweets.return_value = mock_tweets_data

    # 2. Mock the OpenAI service response
    mock_summary_json = {
        "official_news": [{
            "company": "OpenAI",
            "updates": [{
                "detail": "We just released a new model that can summarize text!",
                "link": "https://twitter.com/OpenAI/status/123"
            }]
        }],
        "upcoming_announcements": [],
        "rumors_and_hot_topics": [{
            "theme": "Rumors about a new AI chip from Google.",
            "sources": ["https://twitter.com/TechCrunch/status/456"]
        }]
    }
    mock_choice = MockChoice(json.dumps(mock_summary_json))
    mock_openai_create.return_value = type("MockResponse", (), {"choices": [mock_choice]})()

    # 3. Call the API endpoint
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/generate-news",
            json={
                "twitter_links": ["https://twitter.com/OpenAI", "https://twitter.com/TechCrunch"],
                "days": 7,
                "language": "en"
            }
        )

    # 4. Assert the results
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["official_news"][0]["company"] == "OpenAI"
    assert "new model" in response_data["official_news"][0]["updates"][0]["detail"]
    assert response_data["rumors_and_hot_topics"][0]["theme"].startswith("Rumors")

    # Verify that our mocks were called
    mock_get_tweets.assert_called_once()
    mock_openai_create.assert_called_once()
