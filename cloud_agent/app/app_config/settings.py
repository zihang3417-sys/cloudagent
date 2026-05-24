import os
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "agent", ".env")

class Settings(BaseSettings):
    dashscope_api_key: str = "ollama"
    redis_url: str = "redis://localhost:6379"
    milvus_host: str = "localhost"
    milvus_port: int = 19530
    milvus_api_key: str | None = None
    embedding_provider: str = "dashscope"
    
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra='ignore')

settings = Settings()
