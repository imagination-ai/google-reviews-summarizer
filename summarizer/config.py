from pydantic import BaseSettings, validator


class CommonSettings(BaseSettings):
    API_BASE_URL: str = "/api/v1"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    OPENAI_API_KEY: str
    GOOGLE_REVIEWS_API_KEY: str

    class Config:
        case_sensitive = True


settings = CommonSettings(_env_file=".env")
