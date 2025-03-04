import os
from pyperclip import copy
import logging
from dotenv import load_dotenv
from database import get_statistics, get_not_found_sequences
from processing import process_single_file


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOUND_FILES_PATH = os.path.join(BASE_DIR, 'found-files')
LOG_FILE_PATH = os.path.join(BASE_DIR, 'console.log')
ENV_FILE_PATH = os.path.join(BASE_DIR, '.env')


logging.basicConfig(
	level=logging.INFO,
	format='%(message)s',
	datefmt='%d.%m.%Y %H:%M:%S',
	handlers=[
		logging.StreamHandler(),
		logging.FileHandler(LOG_FILE_PATH)
	]
)


def split_array(array: list, chunk_size: int):
	return [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]


def copy_for_reviving():
	not_found = get_not_found_sequences('a', 'a')
	chunks = split_array(not_found, 64)
	data = '\n\n'.join(map(lambda x: f'await revive(`{'\\n'.join(x)}`);', chunks))
	copy(data)


def get_all_stats():
	total_overall, found_overall = 0, 0

	for letter in 'abcdefghijklmnopqrstuvwxyz':
		total, found, percentage = get_statistics(letter)
		logging.info(f'Letter {letter}: {found:<7,} / {total:,} sequences found ({percentage:.2f}%)')

		total_overall += total
		found_overall += found

	overall_percentage = (found_overall / total_overall * 100) if total_overall else 0
	logging.info('\n--- Overall Statistics ---')
	logging.info(f'Total: {found_overall:,} / {total_overall:,} sequences found ({overall_percentage:.2f}%)\n\n')


def process_everything():
	sub_directory = 'other'
	for file_name in os.listdir(os.path.join(FOUND_FILES_PATH, sub_directory)):
		file_path = os.path.join(FOUND_FILES_PATH, sub_directory, file_name)
		process_single_file(file_path)


def main():
	get_all_stats()
	process_everything()
	get_all_stats()


if __name__ == '__main__':
	main()
