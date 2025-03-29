from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    X_BEARER_TOKEN: str = Field(..., env='X_BEARER_TOKEN')
    GEMINI_API_KEY: str = Field(..., env='GEMINI_API_KEY')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
