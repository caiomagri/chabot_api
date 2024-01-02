from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    ENV: str = "DEV"
    TITLE: str = "CHATBOT API"
    VERSION: str = "0.0.1"

    CHATBOT_TYPE: str = "chatgpt"

    CHATBOT_NAME: str = "Charlie"
    CHATBOT_STORAGE_ADAPTER: str = "chatterbot.storage.SQLStorageAdapter"
    CHATBOT_DATABASE_URI: str = "sqlite:///database.sqlite3"

    # OpenAI
    OPENAI_TOKEN: str = Field(default=None)
    OPENAI_API_BASE: str = ""
    OPENAI_API_VERSION: str = ""
    OPENAI_CHAT_MODEL: str = "gpt-3.5-turbo"
    OPENAI_API_TYPE: str = ""
    OPENAI_TEMPERATURE: float = 0.4
    OPENAI_TOP_P: float = 1
    OPENAI_FREQUENCY_PENALTY: float = 0.4
    OPENAI_PRESENCE_PENALTY: float = 0.4
    OPENAI_MAX_TOKENS: int = 1000
    OPENAI_TIMEOUT: int = 30
