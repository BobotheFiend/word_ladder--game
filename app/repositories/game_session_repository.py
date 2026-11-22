from abc import ABC, abstractmethod
from app.schemas import GameSession


class GameSessionRepository(ABC):

    @abstractmethod
    def save_game_session(self, game_session: GameSession) -> GameSession:
        pass

    @abstractmethod
    def get_game_session_by_id(self, game_session_id: str) -> GameSession | None:
        pass

    @abstractmethod
    def update_game_session(self, game_session: GameSession) -> GameSession:
        pass
