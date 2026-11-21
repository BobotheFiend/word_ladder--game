from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import SQLModel, create_engine


class Settings(BaseSettings):
    WORD_LADDER: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
settings = Settings()

engine = create_engine(
    settings.WORD_LADDER,
    echo=True,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)