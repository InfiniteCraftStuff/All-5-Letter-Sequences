import sqlite3
import os
from typing import LiteralString, NamedTuple
from collections.abc import Iterable
import logging


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)

DB_FILE = os.path.join(BASE_DIR, "databases", "database.db")


def connect_db():
    return sqlite3.connect(DB_FILE)


def get_is_found(sequence: LiteralString) -> bool | None:
    sequence = sequence.lower()  # Convert sequence to lowercase before processing
    if len(sequence) != 5:
        raise ValueError("Sequence must be 5 letters")

    query = "SELECT found FROM sequences WHERE sequence = ?"

    with connect_db() as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, (sequence,)).fetchone()
        return bool(result[0]) if result else None


def update_sequences(sequences: Iterable[str], is_found: bool = True):
    if not sequences:
        return

    query = "UPDATE sequences SET found = ? WHERE sequence = ?"

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.executemany(
            query, ((is_found, seq.lower()) for seq in sequences)
        )  # Ensure sequences are lowercase
        conn.commit()


def get_sequences_from_file(file_path: str) -> list[str]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [
                line.strip().lower() for line in file if line.strip()
            ]  # Convert to lowercase while reading
    except FileNotFoundError:
        logging.warning(f"File not found: {file_path}")
        return []


def get_not_found_sequences() -> list[str]:
    query = "SELECT sequence FROM sequences WHERE found = 0"

    with connect_db() as conn:
        cursor = conn.cursor()
        sequences = cursor.execute(query).fetchall()
        return [seq[0] for seq in sequences]


class Stats(NamedTuple):
    total: int
    found: int
    percentage: float


def get_statistics() -> Stats:
    with connect_db() as conn:
        cursor = conn.cursor()
        total_query = "SELECT COUNT(*) FROM sequences"
        found_query = "SELECT COUNT(*) FROM sequences WHERE found = 1"

        total = cursor.execute(total_query).fetchone()[0]
        found = cursor.execute(found_query).fetchone()[0]

        percentage = (found / total * 100) if total else 0
        return Stats(total, found, percentage)
