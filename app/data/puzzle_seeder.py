import json
from pathlib import Path
from sqlmodel import Session, select
from app.schemas import Puzzle

PUZZLES_FILE = Path(__file__).resolve().parent / "puzzles.json"


def seed_initial_puzzles(db: Session, json_path: Path = PUZZLES_FILE) -> None:
    existing_pairs = {
        (gotten.upper(), target.upper())
        for gotten, target in db.exec(
            select(Puzzle.gotten_word, Puzzle.target_word)
        ).all()
    }

    with json_path.open("r", encoding="utf-8") as f:
        raw_puzzles = json.load(f)

    new_puzzles = [
        Puzzle(
            gotten_word=item["gotten_word"].upper(),
            target_word=item["target_word"].upper(),
            word_length=item["word_length"],
            steps=item["steps"],
        )
        for item in raw_puzzles
        if (item["gotten_word"].upper(), item["target_word"].upper()) not in existing_pairs
    ]

    if new_puzzles:
        db.add_all(new_puzzles)
        db.commit()
