from langchain_anthropic import ChatAnthropic
from app.config import settings

def get_llm(temp = 0.7):
    return ChatAnthropic(
        model=settings.model,
        api_key=settings.api_key,
        temperature=temp
    )