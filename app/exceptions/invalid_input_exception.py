from app.exceptions.word_ladder_exception import WordLadderException
from fastapi import status

class InvalidInputException(WordLadderException):

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)