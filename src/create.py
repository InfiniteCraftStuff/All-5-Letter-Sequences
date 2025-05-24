import sqlite3
import string
import os


def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    for first_letter in string.ascii_lowercase:
        DB_PATH = os.path.join(BASE_DIR, "databases", "sequences", f"{first_letter}.db")
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            for second_letter in string.ascii_lowercase:
                table_name = f"{first_letter}{second_letter}"
                cursor.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS "{table_name}" (
                        sequence TEXT PRIMARY KEY,
                        found  BOOLEAN DEFAULT FALSE
                    )
                    """
                )

            conn.commit()


if __name__ == "__main__":
    main()
