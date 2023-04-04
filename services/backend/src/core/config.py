from pydantic import BaseSettings
from typing import Optional

DEFAULT_SECRET_KEY = "chat-note"

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 18080


class Settings(BaseSettings):
    debug: bool = False

    # server start at `host:port`.
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT

    database_url: Optional[str] = None
    secret_key: Optional[str] = DEFAULT_SECRET_KEY

    # openai
    openai_api_key: str = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # env_nested_delimiter = "__"


settings = Settings()


if __name__ == "__main__":
    from pprint import pprint

    pprint(settings.dict())
