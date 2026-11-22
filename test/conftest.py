import pytest
from sqlmodel import create_engine, Session, SQLModel
import app.schemas.models
from app.repositories import GameSessionRepositoryImpl, GameSessionRepository, PuzzleRepositoryImpl, PuzzleRepository

TEST_DATABASE_URL: str = "sqlite:///./word_ladder_test.db"

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 5}
)


@pytest.fixture
def db_session():
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session

@pytest.fixture
def puzzle_repository(db_session: Session) -> PuzzleRepository:
    return PuzzleRepositoryImpl(database_session=db_session)


@pytest.fixture
def game_session_repository(db_session:Session) -> GameSessionRepository:
    return GameSessionRepositoryImpl(database_session=db_session)