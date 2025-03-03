import sqlite3
import os
from typing import Iterable
import logging


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_SEQUENCES_PATH = os.path.join(BASE_DIR, 'databases', 'sequences')


def connect_db(letter: str):
	return sqlite3.connect(os.path.join(DB_SEQUENCES_PATH, f'{letter}.db'))


def get_is_found(sequence: str) -> bool | None:
	sequence = sequence.lower()  # Convert sequence to lowercase before processing
	if len(sequence) != 5:
		raise ValueError('Sequence must be 5 letters')

	table_name = f'"{sequence[:2]}"'
	query = f'SELECT found FROM {table_name} WHERE sequence = ?'

	with connect_db(sequence[0]) as conn:
		cursor = conn.cursor()
		result = cursor.execute(query, (sequence,)).fetchone()
		return bool(result[0]) if result else None


def update_sequences(letter: str, sequences: Iterable[str], is_found=True):
	if not sequences:
		return

	table_name = f'"{sequences[0][:2]}"'
	query = f'UPDATE {table_name} SET found = ? WHERE sequence = ?'

	with connect_db(letter) as conn:
		cursor = conn.cursor()
		cursor.executemany(query, ((is_found, seq.lower()) for seq in sequences))  # Ensure sequences are lowercase
		conn.commit()


def get_sequences_from_file(file_rel_path: Iterable[str]) -> list[str]:
	file_path = os.path.join(BASE_DIR, *file_rel_path)
	try:
		with open(file_path, 'r') as file:
			return [line.strip().lower() for line in file if line.strip()]  # Convert to lowercase while reading
	except FileNotFoundError:
		logging.warning(f'File not found: {file_path}')
		return []


def get_not_found_sequences(letter: str, second_letter: str) -> list[str]:
    table_name = f'"{letter}{second_letter}"'
    query = f'SELECT sequence FROM {table_name} WHERE found = 0'

    with connect_db(letter) as conn:
        cursor = conn.cursor()
        sequences = cursor.execute(query).fetchall()
        return [seq[0] for seq in sequences]


def get_statistics(letter: str):
	with connect_db(letter) as conn:
		cursor = conn.cursor()
		total, found = 0, 0

		for second_letter in 'abcdefghijklmnopqrstuvwxyz':
			table_name = f'"{letter}{second_letter}"'
			total_query = f'SELECT COUNT(*) FROM {table_name}'
			found_query = f'SELECT COUNT(*) FROM {table_name} WHERE found = 1'

			total += cursor.execute(total_query).fetchone()[0]
			found += cursor.execute(found_query).fetchone()[0]

		percentage = (found / total * 100) if total else 0
		return total, found, percentage
