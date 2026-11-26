from functools import lru_cache
from pathlib import Path
from typing import Annotated, Generator

from app.config.settings import engine
from app.repositories import (
    GameSessionRepository,
    GameSessionRepositoryImpl,
    PuzzleRepository,
    PuzzleRepositoryImpl,
)
from app.services import DictionaryService, GamingService, GamingServiceImpl
from fastapi import Depends
from sqlmodel import Session


def get_db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@lru_cache
def get_dictionary_service() -> DictionaryService:
    service = DictionaryService()
    dict_path = Path(__file__).resolve().parent / "data" / "words.txt"
    service.load_from_file(dict_path)
    return service


def get_puzzle_repository(
        db: Annotated[Session, Depends(get_db_session)],
) -> PuzzleRepository:
    return PuzzleRepositoryImpl(db)


def get_game_session_repository(
        db: Annotated[Session, Depends(get_db_session)],
) -> GameSessionRepository:
    return GameSessionRepositoryImpl(db)


def get_gaming_service(
        puzzle_repo: Annotated[PuzzleRepository, Depends(get_puzzle_repository)],
        session_repo: Annotated[
            GameSessionRepository, Depends(get_game_session_repository)
        ],
        dictionary_service: Annotated[
            DictionaryService, Depends(get_dictionary_service)
        ],
) -> GamingService:
    return GamingServiceImpl(
        puzzle_repository=puzzle_repo,
        game_session_repository=session_repo,
        dictionary_service=dictionary_service,
    )
