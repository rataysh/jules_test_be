import pytest
from unittest.mock import patch, AsyncMock
from app.services.openai_service import get_news_from_openai
from app.api.schemas import NewsRequest

# A mock for the choice object in the OpenAI response
class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockMessage:
    def __init__(self, content):
        self.content = content

@pytest.mark.asyncio
@patch("app.services.openai_service.client.chat.completions.create", new_callable=AsyncMock)
async def test_get_news_from_openai(mock_create):
    """
    Test that the prompt is constructed correctly and the OpenAI API is called.
    """
    # Mock the response from OpenAI
    mock_response_content = "Test response"
    mock_choice = MockChoice(mock_response_content)
    mock_create.return_value = type("MockResponse", (), {"choices": [mock_choice]})()

    # Create a sample request
    request = NewsRequest(
        twitter_links=["http://twitter.com/test"],
        days=1,
        language="English"
    )

    # Call the function
    result = await get_news_from_openai(request)

    # Assertions
    assert result == mock_response_content
    mock_create.assert_called_once()

    # Check that the prompt was formatted correctly
    call_args, call_kwargs = mock_create.call_args
    assert call_kwargs["model"] == "gpt-5-nano-2025-08-07"
    messages = call_kwargs.get("messages", [])
    user_message = next((m for m in messages if m["role"] == "user"), None)

    assert user_message is not None
    assert "http://twitter.com/test" in user_message["content"]
    assert "Default: 1" in user_message["content"]
    assert "Default: English" in user_message["content"]
