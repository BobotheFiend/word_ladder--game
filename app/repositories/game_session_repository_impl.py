from app.schemas import GameSession
from sqlmodel import Session
from .game_session_repository import GameSessionRepository


class GameSessionRepositoryImpl(GameSessionRepository):

    def __init__(self, database_session: Session):
        self.data_base = database_session

    def save_game_session(self, game_session: GameSession) -> GameSession:
        self.data_base.add(game_session)
        self.data_base.commit()
        self.data_base.refresh(game_session)
        return game_session

    def get_game_session_by_id(self, game_session_id: str) -> GameSession | None:
        return self.data_base.get(GameSession, game_session_id)

    def update_game_session(self, game_session: GameSession) -> GameSession:
        self.data_base.add(game_session)
        self.data_base.commit()
        self.data_base.refresh(game_session)
        return game_session
