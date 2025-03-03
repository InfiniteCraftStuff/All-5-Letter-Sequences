import os
from time import time
from typing import Iterable
import logging
from database import update_sequences, get_sequences_from_file


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOUND_FILES_PATH = os.path.join(BASE_DIR, 'found-files')


def process_batch(letter: str, sequences: list[str]):
	grouped_sequences: list[list[str]] = [[] for _ in range(26)]

	for seq in sequences:
		seq = seq.lower()
		grouped_sequences[ord(seq[1]) - 97].append(seq)

	for batch in grouped_sequences:
		if batch:
			logging.info(f'Processing batch {batch[0][:2]} ({len(batch)} sequences)')
			batch_start = time()
			update_sequences(letter, batch)
			logging.info(f'Batch {batch[0][:2]} processed in {time() - batch_start:.2f} seconds')


def process_letter(letter: str, sequences: list[str]):
	logging.info(f'\n--- Processing sequences for letter {letter} ---')
	start_time = time()

	process_batch(letter, sequences)
	logging.info(f'--- Completed letter {letter} in {time() - start_time:.2f} seconds ---\n')


def process_directory_by_letter(subdirectory_name: str):
	"""Process directory where files are already separated by letters."""
	logging.info(f'\n--- Processing directory {subdirectory_name} where files are separated by letter ---')

	for letter in 'abcdefghijklmnopqrstuvwxyz':
		file_rel_path = subdirectory_name, f'{letter}.txt'
		sequences = get_sequences_from_file(file_rel_path)
		if sequences:
			process_letter(letter, sequences)


def process_single_file(file_rel_path: Iterable[str]):
	"""Process a single file, splitting sequences by letter and then processing them."""
	logging.info(f'\n--- Processing single file: {file_rel_path[-1]} ---')

	sequences = get_sequences_from_file(file_rel_path)
	if not sequences:
		logging.info('No sequences found. Skipping.\n')
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
			logging.info(f'Processing batch for letter {letter} ({len(batch)} sequences)')
			process_letter(letter, batch)
