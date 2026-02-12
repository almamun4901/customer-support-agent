from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    api_key: str = Field(alias="ANTHROPIC_API_KEY")
    model: str = Field(default="claude-3-5-sonnet-20241022", alias="CLAUDE_MODEL")
    database_url: str = Field(alias="DATABASE_URL")

    class Config:
        env_file = ".env"
        populate_by_name = True
        extra = "ignore"

settings = Settings()
