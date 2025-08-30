from fastapi import APIRouter
from app.api.schemas import NewsRequest, NewsResponse
from app.services.openai_service import get_news_from_openai

router = APIRouter()

@router.post("/generate-news", response_model=NewsResponse, status_code=200)
async def generate_news(request: NewsRequest) -> NewsResponse:
    """
    Generate a news summary based on the provided sources.
    """
    summary_data = await get_news_from_openai(request)
    return summary_data
