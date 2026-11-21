from app.schemas.models.enums import GameMode, Status
from pydantic import BaseModel


class StartGameResponse(BaseModel):
    session_id: str
    mode: GameMode
    status: Status
    gotten_word: str
    target_word: str
    max_moves: int | None = None
    time_limit_seconds: int | None = None
    message: str
