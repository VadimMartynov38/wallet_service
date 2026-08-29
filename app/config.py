import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: Optional[str] = None


settings = Settings()
