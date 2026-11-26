from typing import Annotated

from app.dependencies import get_gaming_service
from app.schemas import (
    StartGameRequest,
    StartGameResponse,
    SubmitLetterRequest,
    SubmitLetterResponse,
)
from app.services import GamingService
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/api/v1/game", tags=["Word Ladder Game"])


@router.post(
    "/start",
    response_model=StartGameResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_game(
        request: StartGameRequest,
        gaming_service: Annotated[GamingService, Depends(get_gaming_service)],
) -> StartGameResponse:
    return gaming_service.start_game(request)


@router.post(
    "/move",
    response_model=SubmitLetterResponse,
    status_code=status.HTTP_200_OK,
)
def submit_move(
        request: SubmitLetterRequest,
        gaming_service: Annotated[GamingService, Depends(get_gaming_service)],
) -> SubmitLetterResponse:
    return gaming_service.submit_move(request)
