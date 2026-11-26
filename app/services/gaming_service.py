from abc import ABC, abstractmethod
from app.schemas import (StartGameRequest,StartGameResponse,SubmitLetterRequest,SubmitLetterResponse,)


class GamingService(ABC):

    @abstractmethod
    def start_game(self, request: StartGameRequest) -> StartGameResponse:
        ...

    @abstractmethod
    def submit_move(self, request: SubmitLetterRequest) -> SubmitLetterResponse:
        ...
