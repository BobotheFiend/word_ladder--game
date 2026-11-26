from app.exceptions import WordLadderException
from fastapi import status

class WordInputException(WordLadderException):

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_406_NOT_ACCEPTABLE)