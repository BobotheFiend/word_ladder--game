from contextlib import asynccontextmanager

from app.config.settings import engine
from app.controllers.game_controller import router as game_router
from app.data.puzzle_seeder import seed_initial_puzzles
from app.dependencies import get_dictionary_service
from app.exceptions import WordLadderException
import app.schemas.models
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session, SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)

    get_dictionary_service()

    with Session(engine) as session:
        seed_initial_puzzles(session)

    yield


app = FastAPI(
    title="Word Ladder Game API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(WordLadderException)
async def word_ladder_exception_handler(request: Request, exc: WordLadderException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


app.include_router(game_router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
