import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TWITTER_USERNAME: str
    TWITTER_COOKIES_FILE: str = "cookies.json"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
