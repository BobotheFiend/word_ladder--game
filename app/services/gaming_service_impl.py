import random
import string
from datetime import datetime, timezone
from typing import override
from fastapi import status
from .dictionary_service import DictionaryService
from .gaming_service import GamingService
from ..exceptions import WordLadderException, InvalidInputException
from ..exceptions.puzzle_exception import PuzzleException
from ..exceptions.word_input_exception import WordInputException
from ..repositories import PuzzleRepository, GameSessionRepository
from app.schemas import SubmitLetterRequest, SubmitLetterResponse, StartGameRequest, StartGameResponse, Puzzle, \
    GameMode, GameSession, Status
from app.utils import Validator


class GamingServiceImpl(GamingService):

    def __init__(self,
                 puzzle_repository: PuzzleRepository,
                 game_session_repository: GameSessionRepository,
                 dictionary_service: DictionaryService
                 ):
        self.puzzle_repository = puzzle_repository
        self.game_session_repository = game_session_repository
        self.dictionary = dictionary_service
        self.DEFAULT_TIME_LIMIT_SECONDS = 60
        self.HARDCORE_EXTRA_MOVES = 2




    @override
    def start_game(self, request: StartGameRequest) -> StartGameResponse:
            Validator.validate(request)

            puzzle = self._pick_puzzle(request.word_length)

            max_moves, time_limit = self._configure_mode_limits(request.mode, puzzle)

            save_to_game_session = self._create_and_save_session(puzzle, request.mode, max_moves, time_limit)

            response = StartGameResponse(
                session_id=save_to_game_session.id,
                mode=save_to_game_session.mode,
                status=save_to_game_session.status,
                gotten_word=save_to_game_session.current_word,
                target_word=save_to_game_session.target_word,
                max_moves=save_to_game_session.max_moves,
                time_limit_seconds=save_to_game_session.time_limit_seconds,
                message=f"Transform '{save_to_game_session.current_word}' into '{save_to_game_session.target_word}'!",
            )
            return response


    @override
    def submit_move(self, request: SubmitLetterRequest) -> SubmitLetterResponse:
        Validator.validate(request)

        session = self._get_active_session(request.session_id)
        guess = request.guess_word.strip().upper()

        return self._validate_game_session(session, guess)


    def _validate_game_session(self, session:GameSession, guess:str)->SubmitLetterResponse:
        if session.mode == GameMode.CLASSIC:
            return self._handle_classic_move(session, guess)
        if session.mode == GameMode.TIME_ATTACK:
            return self._handle_time_attack_move(session, guess)
        if session.mode == GameMode.HARDCORE:
            return self._handle_hardcore_move(session, guess)
        else:
            raise WordLadderException(f"Unsupported game mode: {session.mode}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)






    def _create_and_save_session(self,puzzle: Puzzle,mode: GameMode,max_moves: int | None,time_limit: int | None,) -> GameSession:
        new_game_session = GameSession(
            puzzle_id=puzzle.id,
            mode=mode,
            current_word=puzzle.gotten_word,
            target_word=puzzle.target_word,
            path_history=[puzzle.gotten_word],
            max_moves=max_moves,
            time_limit_seconds=time_limit,
        )
        return self.game_session_repository.save_game_session(new_game_session)

    def _pick_puzzle(self, requested_length: int | None) -> Puzzle:
        available_lengths = self.puzzle_repository.get_available_word_lengths()
        if not available_lengths:
            raise PuzzleException("Puzzle board is empty: no puzzles loaded")

        word_length = (
            requested_length
            if requested_length in available_lengths
            else random.choice(available_lengths)
        )

        puzzle = self.puzzle_repository.get_puzzles_by_random(word_length=word_length)
        if not puzzle:
            raise PuzzleException(f"No puzzle found for length {word_length}")
        return puzzle

    def _configure_mode_limits(self, mode: GameMode, puzzle: Puzzle) -> tuple[int | None, int | None]:
        if mode == GameMode.HARDCORE:
            return puzzle.steps + self.HARDCORE_EXTRA_MOVES, None
        if mode == GameMode.TIME_ATTACK:
            return None, self.DEFAULT_TIME_LIMIT_SECONDS
        return None, None



    def _handle_classic_move(self, session: GameSession, guess: str) -> SubmitLetterResponse:
        message = self._apply_core_rules_and_move(session, guess)
        self.game_session_repository.save_game_session(session)
        return self._response_after_every_move(session, message)

    def _handle_time_attack_move(self, session: GameSession, guess: str) -> SubmitLetterResponse:
        time_remaining = self._check_time_remaining(session)
        if time_remaining is not None and time_remaining <= 0:
            session.status = Status.TIME_UP
            self.game_session_repository.save_game_session(session)
            return self._response_after_every_move(session, "Time's up! You ran out of time.", time_remaining=0.0)

        message = self._apply_core_rules_and_move(session, guess)
        self.game_session_repository.save_game_session(session)
        return self._response_after_every_move(session, message, time_remaining=time_remaining)

    def _handle_hardcore_move(
            self, session: GameSession, guess: str
    ) -> SubmitLetterResponse:
        message = self._apply_core_rules_and_move(session, guess)

        if self._is_out_of_moves(session):
            session.status = Status.NO_MOVES_LEFT
            message = (f"Game Over! You reached the limit of {session.max_moves} moves.")

        self.game_session_repository.save_game_session(session)
        return self._response_after_every_move(session, message)


    def _apply_core_rules_and_move(self, session: GameSession, guess: str) -> str:
        self._validate_guess_rules(session, guess)
        self._record_move(session, guess)

        if self._check_win(session):
            return f"Congratulations! Solved in {session.moves_used} moves!"

        if self._check_land_of_no_return(session):
            return f"LAND OF NO RETURN! {session.current_word} has no valid moves left."

        return "Valid move!"

    def _get_active_session(self, session_id: str) -> GameSession:
        session = self.game_session_repository.get_game_session_by_id(session_id)
        if not session:
            raise WordLadderException(message="Game session not found.",status_code=status.HTTP_404_NOT_FOUND,)
        if session.status != Status.IN_PROGRESS:
            raise WordLadderException(message=f"Game already ended with status: {session.status.value}",status_code=status.HTTP_400_BAD_REQUEST)
        return session


    def _validate_guess_rules(self, session: GameSession, guess: str) -> None:
        if guess in session.path_history:
            raise WordInputException(f"You already used '{guess}' in this round.")
        if not self._is_one_letter_diff(session.current_word, guess):
            raise InvalidInputException("Invalid move: Changes To Word Can Only Happen One Letter At A Time!")
        if not self.dictionary.is_valid_word(guess):
            raise WordLadderException(f"'{guess}' Word Not found.")

    def _record_move(self, session: GameSession, guess: str) -> None:
        session.current_word = guess
        session.path_history = [*session.path_history, guess]
        session.moves_used += 1

    def _check_win(self, session: GameSession) -> bool:
        if session.current_word == session.target_word:
            session.status = Status.WON
            return True
        return False

    def _check_land_of_no_return(self, session: GameSession) -> bool:
        if not self._has_valid_moves_left(session.current_word, session.path_history):
            session.status = Status.LAND_OF_NO_RETURN
            return True
        return False

    def _is_out_of_moves(self, session: GameSession) -> bool:
        return (session.status == Status.IN_PROGRESS and session.max_moves is not None
                and session.moves_used >= session.max_moves)



    def _check_time_remaining(self, session: GameSession) -> float | None:
        if (session.mode != GameMode.TIME_ATTACK or session.time_limit_seconds is None):
            return None

        created_at = (session.created_at.replace(tzinfo=timezone.utc)
        if session.created_at.tzinfo is None
        else session.created_at
        )

        elapsed = (datetime.now(timezone.utc) - created_at).total_seconds()
        return round(session.time_limit_seconds - elapsed, 1)



    def _is_one_letter_diff(self, word1: str, word2: str) -> bool:
        """Checks that two words have the same length and differ by strictly 1 letter."""
        if len(word1) != len(word2):
            return False
        return sum(1 for a, b in zip(word1.upper(), word2.upper()) if a != b) == 1



    def _has_valid_moves_left(self, current_word: str, visited: list[str]) -> bool:
        """Powers 'Land of No Return': returns False if zero unused valid words are 1 letter away."""
        current_word = current_word.upper()
        visited_set = {word.upper() for word in visited}

        for i in range(len(current_word)):
            for letter in string.ascii_uppercase:
                if letter == current_word[i]:
                    continue
                candidate = current_word[:i] + letter + current_word[i + 1 :]
                if candidate not in visited_set and self.dictionary.is_valid_word(candidate):
                    return True
        return False



    def _response_after_every_move(self, session: GameSession, message: str, time_remaining: float | None = None, ) -> SubmitLetterResponse:
        moves_remaining = (
            max(0, session.max_moves - session.moves_used)
            if session.max_moves is not None
            else None
        )

        return SubmitLetterResponse(
            session_id=session.id,
            status=session.status,
            current_word=session.current_word,
            path_history=session.path_history,
            moves_used=session.moves_used,
            moves_remaining=moves_remaining,
            time_remaining_seconds=time_remaining,
            message=message,
        )

