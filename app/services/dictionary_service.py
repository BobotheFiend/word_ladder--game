from pathlib import Path


class DictionaryService:

    def __init__(self):
        self._words_by_length: dict[int, set[str]] = {}

    def load_from_file(self, file_path: str | Path) -> None:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Dictionary file not found at: {path}")

        with path.open("r", encoding="utf-8") as file:
            words = {line.strip().upper() for line in file if line.strip()}
        self.filter_words_in_dictionary(words)

    def filter_words_in_dictionary(self, words: set[str] | None) -> None:
        self._words_by_length.clear()
        if not words:
            return

        for raw_word in words:
            word = raw_word.strip().upper()
            if word.isalpha() and 3 <= len(word) <= 7:
                self._words_by_length.setdefault(len(word), set()).add(word)

    def is_valid_word(self, word: str | None) -> bool:
        if not word:
            return False
        cleaned = word.strip().upper()
        return cleaned in self._words_by_length.get(len(cleaned), set())
