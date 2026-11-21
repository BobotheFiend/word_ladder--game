from app.schemas.models.enums import Status
from pydantic import BaseModel


class SubmitLetterResponse(BaseModel):
    session_id: str
    status: Status
    current_word: str
    path_history: list[str]
    moves_used: int
    moves_remaining: int | None = None
    time_remaining_seconds: float | None = None
    message: str
