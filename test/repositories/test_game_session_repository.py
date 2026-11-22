from app.repositories import GameSessionRepository, PuzzleRepository
from app.schemas import Puzzle, GameSession, GameMode, Status


class TestGameSessionRepository:

    def test_save_game_session(self,
                               game_session_repository: GameSessionRepository,
                               puzzle_repository: PuzzleRepository
                               ):

        puzzle = puzzle_repository.save_puzzle(
            Puzzle(gotten_word="SOAK", target_word="BOAT", word_length=4, steps=2)
        )

        game_session = GameSession(
            puzzle_id=puzzle.id,
            mode=GameMode.CLASSIC,
            current_word="SOAK",
            target_word="BOAT",
            path_history=["SOAK"],
        )
        saved_session = game_session_repository.save_game_session(game_session)

        assert saved_session.id is not None
        assert saved_session.status == Status.IN_PROGRESS
        assert saved_session.path_history == ["SOAK"]

    def test_get_game_session(self,game_session_repository: GameSessionRepository,
                              puzzle_repository: PuzzleRepository):
        puzzle = puzzle_repository.save_puzzle(
            Puzzle(
                gotten_word="BROWN",
                target_word="THROW",
                word_length=5,
                steps=3
            )
        )

        game_session = GameSession(
            puzzle_id=puzzle.id,
            mode=GameMode.CLASSIC,
            current_word="BROWN",
            target_word="THROW",
            path_history=["BROWN"],
        )

        saved_session = game_session_repository.save_game_session(game_session)

        found_session = game_session_repository.get_game_session_by_id(saved_session.id)

        assert found_session.target_word == "THROW"
        assert found_session.id == saved_session.id
        assert found_session.created_at == saved_session.created_at