from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    model: str = "claude-3-5-sonnet-20241022"
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
