import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "smart_ai_db")
    
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_URL: str = os.getenv("DEEPSEEK_API_URL")
    
    GITHUB_API_URL: str = "https://api.github.com"
    
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Settings()