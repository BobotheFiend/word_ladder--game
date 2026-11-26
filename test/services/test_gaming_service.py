from datetime import datetime, timedelta, timezone
from app.exceptions import (
    InvalidInputException,
    PuzzleException,
    WordInputException,
    WordLadderException,
)
from app.repositories import GameSessionRepository, PuzzleRepository
from app.schemas import (
    GameMode,
    Puzzle,
    StartGameRequest,
    Status,
    SubmitLetterRequest,
)
from app.services import DictionaryService, GamingServiceImpl
import pytest


class TestGamingService:

    @pytest.fixture
    def dictionary_service(self) -> DictionaryService:
        service = DictionaryService()
        service.filter_words_in_dictionary(
            {"SOAK", "SOAT", "BOAT", "SOCK", "COAT", "GOAT", "MOAT"}
        )
        return service


    def test_start_game_request_is_none_raises_exception(self, gaming_service: GamingService):
        with pytest.raises(InvalidInputException):
            gaming_service.start_game(None)

    def test_start_game_empty_board_raises_puzzle_exception(
            self, gaming_service: GamingServiceImpl
    ):
        with pytest.raises(PuzzleException):
            gaming_service.start_game(StartGameRequest(mode=GameMode.CLASSIC))

    def test_classic_mode_win_flow(
            self,
            gaming_service: GamingServiceImpl,
            puzzle_repository: PuzzleRepository,
    ):
        puzzle_repository.save_puzzle(
            Puzzle(gotten_word="SOAK", target_word="BOAT", word_length=4, steps=2)
        )

        started = gaming_service.start_game(
            StartGameRequest(mode=GameMode.CLASSIC, word_length=4)
        )
        assert started.gotten_word == "SOAK"
        assert started.max_moves is None

        move1 = gaming_service.submit_move(
            SubmitLetterRequest(session_id=started.session_id, guess_word="SOAT")
        )
        assert move1.status == Status.IN_PROGRESS
        assert move1.moves_used == 1

        move2 = gaming_service.submit_move(
            SubmitLetterRequest(session_id=started.session_id, guess_word="BOAT")
        )
        assert move2.status == Status.WON
        assert move2.path_history == ["SOAK", "SOAT", "BOAT"]

    def test_rejects_repeated_word_multi_letter_and_unknown_word(
            self,
            gaming_service: GamingServiceImpl,
            puzzle_repository: PuzzleRepository,
    ):
        puzzle_repository.save_puzzle(
            Puzzle(gotten_word="SOAK", target_word="BOAT", word_length=4, steps=2)
        )
        started = gaming_service.start_game(
            StartGameRequest(mode=GameMode.CLASSIC, word_length=4)
        )

        with pytest.raises(InvalidInputException):
            gaming_service.submit_move(
                SubmitLetterRequest(session_id=started.session_id, guess_word="BOAT")
            )

        with pytest.raises(WordInputException):
            gaming_service.submit_move(
                SubmitLetterRequest(session_id=started.session_id, guess_word="SOAK")
            )

        with pytest.raises(WordLadderException):
            gaming_service.submit_move(
                SubmitLetterRequest(session_id=started.session_id, guess_word="ZOAK")
            )

    def test_land_of_no_return_triggers_on_dead_end(
            self,
            gaming_service: GamingServiceImpl,
            puzzle_repository: PuzzleRepository,
    ):
        puzzle_repository.save_puzzle(
            Puzzle(gotten_word="SOAK", target_word="BOAT", word_length=4, steps=2)
        )
        started = gaming_service.start_game(
            StartGameRequest(mode=GameMode.CLASSIC, word_length=4)
        )

        dead_end = gaming_service.submit_move(
            SubmitLetterRequest(session_id=started.session_id, guess_word="SOCK")
        )
        assert dead_end.status == Status.LAND_OF_NO_RETURN

    def test_hardcore_mode_enforces_move_limit(
            self,
            gaming_service: GamingServiceImpl,
            puzzle_repository: PuzzleRepository,
    ):
        puzzle_repository.save_puzzle(
            Puzzle(gotten_word="SOAK", target_word="MOAT", word_length=4, steps=1)
        )
        started = gaming_service.start_game(
            StartGameRequest(mode=GameMode.HARDCORE, word_length=4)
        )
        assert started.max_moves == 3

        gaming_service.submit_move(
            SubmitLetterRequest(session_id=started.session_id, guess_word="SOAT")
        )
        gaming_service.submit_move(
            SubmitLetterRequest(session_id=started.session_id, guess_word="COAT")
        )
        final_move = gaming_service.submit_move(
            SubmitLetterRequest(session_id=started.session_id, guess_word="GOAT")
        )

        assert final_move.status == Status.NO_MOVES_LEFT
        assert final_move.moves_remaining == 0

    def test_time_attack_expires_when_time_runs_out(
            self,
            gaming_service: GamingServiceImpl,
            puzzle_repository: PuzzleRepository,
            game_session_repository: GameSessionRepository,
    ):
        puzzle_repository.save_puzzle(
            Puzzle(gotten_word="SOAK", target_word="BOAT", word_length=4, steps=2)
        )
        started = gaming_service.start_game(
            StartGameRequest(mode=GameMode.TIME_ATTACK, word_length=4)
        )

        session = game_session_repository.get_game_session_by_id(started.session_id)
        assert session is not None
        session.created_at = datetime.now(timezone.utc) - timedelta(seconds=65)
        game_session_repository.save_game_session(session)

        late_move = gaming_service.submit_move(
            SubmitLetterRequest(session_id=started.session_id, guess_word="SOAT")
        )
        assert late_move.status == Status.TIME_UP
