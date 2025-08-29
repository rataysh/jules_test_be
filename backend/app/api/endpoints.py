from fastapi import APIRouter, HTTPException
from app.api.schemas import NewsRequest
from app.services.openai_service import get_news_from_openai

router = APIRouter()

@router.post("/generate-news", status_code=200)
async def generate_news(request: NewsRequest):
    """
    Generate a news summary based on the provided sources.
    """
    try:
        summary = await get_news_from_openai(request)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
