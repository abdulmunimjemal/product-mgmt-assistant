from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    X_BEARER_TOKEN: str = Field(..., env='X_BEARER_TOKEN')
    GEMINI_API_KEY: str = Field(..., env='GEMINI_API_KEY')
    MONGODB_URI: str = Field("mongodb://localhost:27017", env="MONGODB_URI")
    MONGODB_DB_NAME: str = Field("workflow_db", env="MONGODB_DB_NAME")
    CELERY_BROKER_URL: str = Field("pyamqp://guest@localhost//", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field("mongodb://localhost:27017", env="CELERY_RESULT_BACKEND")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = "allow"

settings = Settings()
