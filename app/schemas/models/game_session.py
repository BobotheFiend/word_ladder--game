from datetime import datetime, timezone
import uuid
from sqlmodel import Field, SQLModel, JSON, Column
from .enums import Status, GameMode

class GameSession(SQLModel, table=True):
    __tablename__ = "game_sessions"

    id: str = Field(default_factory=lambda: str(uuid.uuid7()), primary_key=True)
    puzzle_id: int = Field(foreign_key="puzzles.id")
    mode: GameMode = Field(index=True)  # classic | time_attack | hardcore
    current_word: str = Field(min_length=3,max_length=7)
    target_word: str = Field(min_length=3,max_length=7)
    path_history: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    moves_used: int = Field(default=0)
    max_moves: int | None = Field(default=None)
    time_limit_seconds: int | None = Field(default=None)
    status: Status = Field(default=Status.IN_PROGRESS, index=True)  # in_progress | won | lost_time | lost_moves | land_of_no_return
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
