from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ID: str = "extraction.app"
    PORT: int = 3000
    MONGODB_URI: str = "mongodb://mongo:27017/extraction"
    GEMINI_API_KEY: str = "<api key>"
    GENERATIVE_MODEL: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
