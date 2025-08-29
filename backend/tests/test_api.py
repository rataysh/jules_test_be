import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock

from app.main import app

# A mock for the choice object in the OpenAI response
class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockMessage:
    def __init__(self, content):
        self.content = content

@pytest.mark.asyncio
@patch("app.services.openai_service.client.chat.completions.create", new_callable=AsyncMock)
async def test_generate_news_success(mock_create):
    """
    Test for successful news generation.
    """
    mock_response_content = "This is a test summary."
    mock_choice = MockChoice(mock_response_content)
    mock_create.return_value = type("MockResponse", (), {"choices": [mock_choice]})()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/generate-news", json={})

    assert response.status_code == 200
    assert response.json() == {"summary": "This is a test summary."}
    mock_create.assert_called_once()
