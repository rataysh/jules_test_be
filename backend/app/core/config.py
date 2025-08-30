import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR points to the 'backend' directory.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from .env file in the base directory
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TWITTER_USERNAME: str
    # Default cookies file path is now absolute, pointing to the project root
    TWITTER_COOKIES_FILE: str = str(BASE_DIR / "cookies.json")

    class Config:
        # Pydantic-settings will automatically override defaults with variables from .env
        env_file = BASE_DIR / ".env"
        case_sensitive = True

settings = Settings()
