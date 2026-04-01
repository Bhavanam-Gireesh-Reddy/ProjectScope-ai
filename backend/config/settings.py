from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    github_token: Optional[str] = None
    groq_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    kaggle_username: Optional[str] = None
    kaggle_key: Optional[str] = None
    
    elasticsearch_host: str = "http://localhost:9200"
    elasticsearch_user: Optional[str] = None
    elasticsearch_password: Optional[str] = None
    
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password123"
    
    mongodb_uri: str = "mongodb://localhost:27017"
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        case_sensitive = False

settings = Settings()
