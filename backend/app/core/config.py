import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/client_updates")
    
    secret_key: str = os.getenv("SECRET_KEY", "your_secret_key_change_this_in_production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    
    api_v1_str: str = "/api/v1"
    project_name: str = "Client Updates Backend"
    
    class Config:
        case_sensitive = False

settings = Settings()