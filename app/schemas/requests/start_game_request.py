from app.schemas.models.enums import GameMode
from pydantic import BaseModel, Field


class StartGameRequest(BaseModel):
    mode: GameMode = Field(default=GameMode.CLASSIC)
    word_length: int | None = Field(default=4, ge=3, le=7)


