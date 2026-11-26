import pytest
from sqlmodel import create_engine, Session, SQLModel
import app.schemas.models
from app.repositories import GameSessionRepositoryImpl, GameSessionRepository, PuzzleRepositoryImpl, PuzzleRepository
from app.services.dictionary_service import DictionaryService
from app.services.gaming_service import GamingService
from app.services.gaming_service_impl import GamingServiceImpl

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

@pytest.fixture
def dictionary_service() -> DictionaryService:
    return DictionaryService()

@pytest.fixture
def gaming_service(puzzle_repository: PuzzleRepository,
                   game_session_repository: GameSessionRepository,
                   dictionary_service: DictionaryService) -> GamingService:
    return GamingServiceImpl(
        puzzle_repository=puzzle_repository,
        game_session_repository=game_session_repository,
        dictionary_service=dictionary_service,
    )
