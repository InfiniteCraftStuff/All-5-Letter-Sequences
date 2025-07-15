import os

import logging

from database import get_statistics, Stats
from processing import process_single_file


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)

FOUND_FILES_PATH = os.path.join(BASE_DIR, "found-files")
LOG_FILE_PATH = os.path.join(BASE_DIR, "logs", "console.log")
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")
STATS_FILE_PATH = os.path.join(BASE_DIR, "STATS.md")


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE_PATH)],
)


def get_all_stats():
    # Initialize variables
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    all_stats: dict[str, Stats] = {}
    total_overall, found_overall = 0, 0

    # Step 1: Collect statistics for all letters
    for letter in letters:
        total, found, percentage = stats = get_statistics(letter)
        all_stats[letter] = stats
        total_overall += total
        found_overall += found
        logging.info(
            f"Letter {letter.upper()}: {found:<7,} / {total:,} sequences found ({percentage:.2f}%)"
        )

    # Calculate overall percentage
    overall_percentage = (found_overall / total_overall * 100) if total_overall else 0
    logging.info("\n--- Overall Statistics ---")
    logging.info(
        f"Total: {found_overall:,} / {total_overall:,} sequences found ({overall_percentage:.2f}%)\n\n"
    )

    # Step 2: Construct the table
    stats_lines = [
        "# Stats\n\n",
        "| Letter | Found    | Percentage | Letter | Found    | Percentage |\n",
        "|--------|----------|------------|--------|----------|------------|\n",
    ]

    # Pair letters: A with N, B with O, ..., M with Z
    for k in range(13):  # 0 to 12 covers all 13 pairs
        letter1 = letters[k]  # A to M (positions 0 to 12)
        letter2 = letters[k + 13]  # N to Z (positions 13 to 25)
        found1, percentage1 = all_stats[letter1][1], all_stats[letter1][2]
        found2, percentage2 = all_stats[letter2][1], all_stats[letter2][2]
        row = (
            f"| {letter1.upper():<6} | {found1:<8,} | {percentage1:>9.2f}% "
            f"| {letter2.upper():<6} | {found2:<8,} | {percentage2:>9.2f}% |\n"
        )
        stats_lines.append(row)

    # Add overall statistics
    stats_lines.append("\n| Total Sequences Found | Percentage |\n")
    stats_lines.append("|-----------------------|------------|\n")
    stats_lines.append(f"| {found_overall:<21,} | {overall_percentage:>9.2f}% |\n")

    # Step 3: Write to STATS.md
    with open(STATS_FILE_PATH, "w") as stats_file:
        stats_file.writelines(stats_lines)


def process_everything():
    for file_name in os.listdir(FOUND_FILES_PATH):
        file_path = os.path.join(FOUND_FILES_PATH, file_name)
        process_single_file(file_path)


def main():
    get_all_stats()
    process_everything()
    get_all_stats()


if __name__ == "__main__":
    main()
