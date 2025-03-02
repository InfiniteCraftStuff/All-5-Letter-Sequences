import sqlite3
import os
from typing import Iterable
from time import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'databases', 'sequences')
FOUND_FILES_PATH = os.path.join(BASE_DIR, 'found-files')


def connect_db(letter: str):
	return sqlite3.connect(os.path.join(DB_PATH, f'{letter}.db'))


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


def get_sequences_from_file(file_path: str) -> list[str]:
	try:
		with open(file_path, 'r') as file:
			return [line.strip().lower() for line in file if line.strip()]  # Convert to lowercase while reading
	except FileNotFoundError:
		print(f'File not found: {file_path}')
		return []


def process_batch(letter: str, sequences: list[str]):
	grouped_sequences = [[] for _ in range(26)]

	for seq in sequences:
		seq = seq.lower()  # Ensure the sequence is lowercase
		grouped_sequences[ord(seq[0]) - 97].append(seq)  # Split by first letter

	for batch in grouped_sequences:
		if batch:
			print(f'Processing batch {batch[0][:2]} ({len(batch)} sequences)')
			batch_start = time()
			update_sequences(letter, batch)
			print(f'Batch {batch[0][:2]} processed in {time() - batch_start:.2f} seconds')


def process_letter(letter: str, sequences: list[str]):
	print(f'\n--- Processing sequences for letter {letter} ---')
	start_time = time()

	process_batch(letter, sequences)
	print(f'--- Completed letter {letter} in {time() - start_time:.2f} seconds ---\n')


def process_directory_by_letter(subdirectory_name: str):
	"""Process directory where files are already separated by letters."""
	print(f'\n--- Processing directory {subdirectory_name} where files are separated by letter ---')

	for letter in 'abcdefghijklmnopqrstuvwxyz':
		file_path = os.path.join(FOUND_FILES_PATH, subdirectory_name, f'{letter}.txt')
		sequences = get_sequences_from_file(file_path)
		if sequences:
			process_letter(letter, sequences)


def process_single_file(file_path: str):
	"""Process a single file, splitting sequences by letter and then processing them."""
	print(f'\n--- Processing single file: {file_path} ---')

	sequences = get_sequences_from_file(file_path)
	if not sequences:
		print('No sequences found. Skipping.\n')
		return

	# Split sequences by letter
	grouped_sequences = [[] for _ in range(26)]
	for seq in sequences:
		seq = seq.lower()  # Ensure sequence is lowercase
		grouped_sequences[ord(seq[0]) - 97].append(seq)

	# Now process each batch of sequences for each letter
	for i, batch in enumerate(grouped_sequences):
		if batch:
			letter = chr(i + 97)  # Convert index to letter
			print(f'Processing batch for letter {letter} ({len(batch)} sequences)')
			process_letter(letter, batch)


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


def get_all_stats():
	total_overall, found_overall = 0, 0

	for letter in 'abcdefghijklmnopqrstuvwxyz':
		total, found, percentage = get_statistics(letter)
		print(f'Letter {letter}: {found:<7,} / {total:,} sequences found ({percentage:.2f}%)')

		total_overall += total
		found_overall += found

	overall_percentage = (found_overall / total_overall * 100) if total_overall else 0
	print(f'\n--- Overall Statistics ---')
	print(f'Total: {found_overall:,} / {total_overall:,} sequences found ({overall_percentage:.2f}%)')


def process_everything():
	file_path = os.path.join(FOUND_FILES_PATH, 'other', 'alive-5-letter-elements-25-03-02-20-56-28.txt')
	process_single_file(file_path)


def main():
	process_everything()
	get_all_stats()


if __name__ == '__main__':
	main()
