from pathlib import Path

import pytest

from app.exceptions import InvalidInputException
from app.services.dictionary_service import DictionaryService


class TestDictionaryService:

    def test_filter_words_in_dictionary_has_a_dictionary_with_only_pure_alphabets_within_the_range_3_to_seven(self, dictionary_service: DictionaryService) -> None:

        words = {
            "yam",
            "123",
            "*^",
            "wheat",
            "foot",
            "sportybet.com",
            "land-rover",
        }

        dictionary_service.filter_words_in_dictionary(words)

        assert 'yam'.upper() in dictionary_service._words_by_length.get(3)
        assert 'foot'.upper() in dictionary_service._words_by_length.get(4)
        assert 'wheat'.upper() in dictionary_service._words_by_length.get(5)
        assert len(dictionary_service._words_by_length.items()) == 3


    def test_word_input_is_valid_return_true(self, dictionary_service: DictionaryService) -> None:
        words = {
            "boat",
            "goat",
            "hay",
            "wheat",
            "stake",
            "sporty",
            "morning",
        }

        dictionary_service.filter_words_in_dictionary(words)

        valid_word = "GOAT"
        is_valid = dictionary_service.is_valid_word(valid_word)

        assert is_valid is True


    def test_word_input_is_invalid_return_false(self, dictionary_service: DictionaryService) -> None:
        words = {
            "boat",
            "goat",
            "hay",
            "wheat",
            "stake",
            "sporty"
            "morning"
        }

        dictionary_service.filter_words_in_dictionary(words)

        invalid_word = "COAT"
        is_not_valid = dictionary_service.is_valid_word(invalid_word)

        assert is_not_valid is False


    def test_load_from_file_from_test_path(self, dictionary_service):
        path = Path(__file__).resolve().parents[1] / "dummy_text_to_test.txt"
        dictionary_service.load_from_file(path)

        assert len(dictionary_service._words_by_length.items()) > 0
        assert "SINGER" in dictionary_service._words_by_length.get(6)
        assert "TIME" in dictionary_service._words_by_length.get(4)