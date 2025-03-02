import sqlite3
import os
from typing import Iterable


class DatabaseManager:
	@staticmethod
	def _get_db_dir(letter):
		base_dir = os.path.dirname(os.path.abspath(__file__))
		return os.path.join(base_dir, 'databases', 'sequences', f'{letter}.db')

	def _connect(self, db_dir: str):
		return sqlite3.connect(db_dir)

	def _fetch(self, db_dir: str, query: str, params=()):
		with self._connect(db_dir) as conn:
			cursor = conn.cursor()
			cursor.execute(query, params)
			return cursor.fetchall()

	def _execute(self, db_dir: str, query: str, params: Iterable[int | float | str | bool | None] = ()):
		with self._connect(db_dir) as conn:
			cursor = conn.cursor()
			cursor.execute(query, params)
			conn.commit()

	def get_is_found(self, sequence: str):
		if len(sequence) != 5:
			raise ValueError('Sequence must be 5 letters')

		sequence = sequence.lower()
		first_letter = sequence[0]
		second_letter = sequence[1]

		db_dir = self._get_db_dir(first_letter)
		table_name = f'"{first_letter}{second_letter}"'

		query = f'SELECT found FROM {table_name} WHERE sequence = ?'
		result = self._fetch(db_dir, query, (sequence,))
		return bool(result[0][0]) if result else None

	def set_is_found(self, sequence: str, is_found=True):
		if len(sequence) != 5:
			raise ValueError('Sequence must be 5 letters')

		sequence = sequence.lower()
		first_letter = sequence[0]
		second_letter = sequence[1]

		db_dir = self._get_db_dir(first_letter)
		table_name = f'"{first_letter}{second_letter}"'

		query = f'UPDATE {table_name} SET found = ? WHERE sequence = ?'
		self._execute(db_dir, query, (is_found,sequence))

	def bulk_set_is_found(self, sequences: Iterable[str], is_found=True):
		for sequence in sequences:
			self.set_is_found(sequence.strip(), is_found)


def main():
	db_manager = DatabaseManager()

	sequences = '''

	'''.strip().split('\n')

	db_manager.bulk_set_is_found(sequences)

if __name__ == '__main__':
	main()
