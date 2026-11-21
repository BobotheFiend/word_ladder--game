import pytest
from sqlmodel import create_engine, Session, SQLModel

TEST_DATABASE_URL: str = "sqlite:///./test.db"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 5})


@pytest.fixture
def session():
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session