import sqlite3
import os
from typing import LiteralString, NamedTuple
from collections.abc import Iterable
import logging


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)

DB_SEQUENCES_PATH = os.path.join(BASE_DIR, "databases", "sequences")


def connect_db(letter: str):
    db_path = os.path.join(DB_SEQUENCES_PATH, f"{letter}.db")
    return sqlite3.connect(db_path)


def get_is_found(sequence: LiteralString) -> bool | None:
    sequence = sequence.lower()  # Convert sequence to lowercase before processing
    if len(sequence) != 5:
        raise ValueError("Sequence must be 5 letters")

    table_name = f'"{sequence[:2]}"'
    query = f"SELECT found FROM {table_name.lower()} WHERE sequence = ?"

    with connect_db(sequence[0]) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, (sequence,)).fetchone()
        return bool(result[0]) if result else None


def update_sequences(letter: str, sequences: Iterable[str], is_found: bool = True):
    if not sequences:
        return

    table_name = f'"{tuple(sequences)[0][:2]}"'
    query = f"UPDATE {table_name} SET found = ? WHERE sequence = ?"

    with connect_db(letter.lower()) as conn:
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


def get_not_found_sequences(letter: str, second_letter: str) -> list[str]:
    table_name = f'"{letter.lower()}{second_letter.lower()}"'
    query = f"SELECT sequence FROM {table_name.lower()} WHERE found = 0"

    with connect_db(letter.lower()) as conn:
        cursor = conn.cursor()
        sequences = cursor.execute(query).fetchall()
        return [seq[0] for seq in sequences]


class Stats(NamedTuple):
    total: int
    found: int
    percentage: float


def get_statistics(letter: LiteralString) -> Stats:
    with connect_db(letter.lower()) as conn:
        cursor = conn.cursor()
        total: int = 0
        found: int = 0

        for second_letter in "abcdefghijklmnopqrstuvwxyz":
            table_name = f'"{letter.lower()}{second_letter}"'
            total_query = f"SELECT COUNT(*) FROM {table_name}"
            found_query = f"SELECT COUNT(*) FROM {table_name} WHERE found = 1"

            total += cursor.execute(total_query).fetchone()[0]
            found += cursor.execute(found_query).fetchone()[0]

        percentage = (found / total * 100) if total else 0
        return Stats(total, found, percentage)
