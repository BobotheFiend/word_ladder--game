from app.schemas import Puzzle
from sqlmodel import Session, select, func
from .puzzle_repository import PuzzleRepository


class PuzzleRepositoryImpl(PuzzleRepository):

    def __init__(self, database_session: Session):
        self.data_base = database_session

    def save_puzzle(self, puzzle: Puzzle) -> Puzzle:
        self.data_base.add(puzzle)
        self.data_base.commit()
        self.data_base.refresh(puzzle)
        return puzzle

    def get_puzzles_by_random(self, word_length: int) -> Puzzle | None:
        random_function_key_word = func.rand()

        if self.data_base.bind.dialect.name == "sqlite":
            random_function_key_word = func.random()

        statement = select(Puzzle)
        statement = statement.where(Puzzle.word_length == word_length)
        statement = statement.order_by(random_function_key_word).limit(1)

        return self.data_base.exec(statement).first()

    def get_puzzle_by_id(self, puzzle_id: int) -> Puzzle | None:
        return self.data_base.get(Puzzle, puzzle_id)

    def get_available_word_lengths(self) -> list[int]:
        statement = select(Puzzle.word_length).distinct()
        return list(self.data_base.exec(statement).all())

    def length(self) -> int:
        query = select(func.count(Puzzle.id))
        return self.data_base.exec(query).one()