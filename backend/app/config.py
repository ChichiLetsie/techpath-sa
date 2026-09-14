from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://techpath:techpath_secret@db:5432/techpath_db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()