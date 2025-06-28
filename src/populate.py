import sqlite3
import itertools
import string
import os


def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    for first_letter in string.ascii_lowercase:
        DB_PATH = os.path.join(BASE_DIR, "databases", "sequences", f"{first_letter}.db")
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            for second_letter in string.ascii_lowercase:
                table_name = f'"{first_letter}{second_letter}"'

                combinations = itertools.product(string.ascii_lowercase, repeat=3)
                sequences = [
                    f'{first_letter}{second_letter}{"".join(combo)}' for combo in combinations
                ]

                cursor.executemany(
                    f"INSERT OR IGNORE INTO {table_name} (sequence) VALUES (?)",
                    ((seq,) for seq in sequences),
                )

            conn.commit()


if __name__ == "__main__":
    main()
