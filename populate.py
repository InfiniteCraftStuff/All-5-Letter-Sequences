import sqlite3
import itertools
import string
import os


base_dir = os.path.dirname(os.path.abspath(__file__))

for first_letter in string.ascii_lowercase:
	db_dir = os.path.join(base_dir, 'databases', 'sequences', f'{first_letter}.db')
	conn = sqlite3.connect(db_dir)
	cursor = conn.cursor()

	for second_letter in string.ascii_lowercase:
		table_name = f'"{first_letter}{second_letter}"'

		combinations = itertools.product(string.ascii_lowercase, repeat=3)
		sequences = [f'{first_letter}{second_letter}{"".join(combo)}' for combo in combinations]

		cursor.executemany(f'INSERT OR IGNORE INTO {table_name} (sequence) VALUES (?)', ((seq,) for seq in sequences))

	conn.commit()
	conn.close()
