import sqlite3
import string
import os


base_dir = os.path.dirname(os.path.abspath(__file__))

for first_letter in string.ascii_lowercase:
	db_dir = os.path.join(base_dir, 'databases', 'sequences', f'{first_letter}.db')
	conn = sqlite3.connect(db_dir)
	cursor = conn.cursor()

	for second_letter in string.ascii_lowercase:
		table_name = f'{first_letter}{second_letter}'
		cursor.execute(f'''
			CREATE TABLE IF NOT EXISTS "{table_name}" (
				sequence TEXT PRIMARY KEY,
				found  BOOLEAN DEFAULT FALSE
			)
		''')

	conn.commit()
	conn.close()
