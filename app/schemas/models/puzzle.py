from sqlmodel import SQLModel, Field


class Puzzle(SQLModel, table=True):

    __tablename__ = "puzzles"

    id: int | None = Field(default=None, primary_key=True)
    gotten_word : str = Field(default=None, min_length=3, max_length=7)
    target_word : str = Field(default=None, min_length=3, max_length=7)
    word_length : int = Field(index=True)
    steps : int

