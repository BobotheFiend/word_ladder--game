from abc import ABC, abstractmethod
from app.schemas import Puzzle

class PuzzleRepository(ABC):
    @abstractmethod
    def save_puzzle(self, puzzle) -> Puzzle:
        pass

    @abstractmethod
    def get_puzzles_by_random(self, word_length: int) -> Puzzle | None:
        pass

    @abstractmethod
    def get_puzzle_by_id(self, puzzle_id) -> Puzzle | None:
        pass

    @abstractmethod
    def get_available_word_lengths(self) -> list[int]:
        ...

    @abstractmethod
    def length(self) -> int:
        ...
