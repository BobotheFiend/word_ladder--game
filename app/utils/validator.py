from typing import overload
from app.exceptions import InvalidInputException
from app.exceptions.word_input_exception import WordInputException
from app.schemas import StartGameRequest, SubmitLetterRequest, GameSession


class Validator:

    @overload
    @staticmethod
    def validate(request: StartGameRequest | None) -> None:
        ...

    @overload
    @staticmethod
    def validate(request: SubmitLetterRequest | None) -> None:
        ...


    @staticmethod
    def validate(request: StartGameRequest | SubmitLetterRequest |  GameSession | None,) -> None:

        if request is None:
            raise InvalidInputException("Invalid Input! Request cannot be Empty")

        if isinstance(request, SubmitLetterRequest):
            if not request.session_id or not request.session_id.strip():
                raise WordInputException("Game Session ID cannot be empty!")
            if not request.guess_word or not request.guess_word.strip():
                raise WordInputException("Guess word cannot be empty!")
            if not request.guess_word.isalpha():
                raise WordInputException("Guess word must only contain letters!")

