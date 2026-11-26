from app.exceptions import WordLadderException
from fastapi import status

class PuzzleException(WordLadderException):

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)