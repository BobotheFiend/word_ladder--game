from app.repositories import PuzzleRepository
from app.schemas import Puzzle


class TestPuzzleRepository:

    def test_save_puzzle_length_is_one(self, puzzle_repository: PuzzleRepository):
        puzzle = Puzzle(
            gotten_word="SOAK", target_word="BOAT", word_length=4, steps=2
        )

        puzzle_repository.save_puzzle(puzzle)

        assert puzzle_repository.length() == 1


    def test_save_puzzle_twice_length_is_two(self, puzzle_repository:PuzzleRepository):

        puzzle = Puzzle(
            gotten_word="SOAK", target_word="BOAT", word_length=4, steps=2
        )

        puzzle_two = Puzzle(
            gotten_word="ONE", target_word="LOL", word_length=3, steps=4
        )

        puzzle_repository.save_puzzle(puzzle)
        puzzle_repository.save_puzzle(puzzle_two)

        assert puzzle_repository.length() == 2

    def test_add_puzzle_find_puzzle_by_id(self, puzzle_repository:PuzzleRepository):
        puzzle = Puzzle(
            gotten_word="WINGS",
            target_word="KNIFE",
            word_length=5,
            steps=4,
        )

        saved_puzzle = puzzle_repository.save_puzzle(puzzle)

        found_puzzle = puzzle_repository.get_puzzle_by_id(saved_puzzle.id)

        assert found_puzzle.id == saved_puzzle.id
        assert found_puzzle.gotten_word == saved_puzzle.gotten_word
        assert found_puzzle.target_word == "KNIFE"


    def test_input_a_word_length_get_random_puzzle_with_same_lenght(self, puzzle_repository:PuzzleRepository):
        puzzle = Puzzle(gotten_word="FLOAT", target_word="STOPS", word_length=5,steps=5)
        puzzle_two = Puzzle(gotten_word="GOAT", target_word="COAT",word_length=4, steps=5)
        puzzle_three = Puzzle(gotten_word="ICE", target_word="DIE", word_length=3, steps=3)
        puzzle_four = Puzzle(gotten_word="MICE", target_word="DICE",word_length=4, steps=4)
        puzzle_five = Puzzle(gotten_word="GRAND", target_word="BRAND",word_length=5, steps=5)
        puzzle_six = Puzzle(gotten_word="KNOWN", target_word="BROWN",word_length=5, steps=5)
        puzzle_seven = Puzzle(gotten_word="SIX", target_word="FLY",word_length=3, steps=3)

        puzzle_repository.save_puzzle(puzzle)
        puzzle_repository.save_puzzle(puzzle_two)
        puzzle_repository.save_puzzle(puzzle_three)
        puzzle_repository.save_puzzle(puzzle_four)
        puzzle_repository.save_puzzle(puzzle_five)
        puzzle_repository.save_puzzle(puzzle_six)
        puzzle_repository.save_puzzle(puzzle_seven)


        gotten_puzzle = puzzle_repository.get_puzzles_by_random(4)
        assert gotten_puzzle.word_length == 4

        gotten_puzzle_two = puzzle_repository.get_puzzles_by_random(5)
        assert gotten_puzzle_two.word_length == 5