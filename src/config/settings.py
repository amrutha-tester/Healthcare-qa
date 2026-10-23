from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_URL: str = "http://localhost:8080"
    DEFAULT_TIMEOUT: float = 20000.0
    HEADLESS: bool = False
    SLOW_MO: float = 0.5

class Config:
    env_file = ".env"

settings = Settings()