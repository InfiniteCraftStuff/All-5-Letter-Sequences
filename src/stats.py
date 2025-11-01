import os.path
import logging

from .database import get_statistics, Stats

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)
STATS_FILE_PATH = os.path.join(BASE_DIR, "STATS.md")


def get_all_stats():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    all_stats: dict[str, Stats] = {}
    total_overall, found_overall = 0, 0

    for letter in letters:
        total, found, _percentage = stats = get_statistics()
        all_stats[letter] = stats
        total_overall += total
        found_overall += found

    overall_percentage = (found_overall / total_overall * 100) if total_overall else 0
    logging.info("\n--- Overall Statistics ---")
    logging.info(
        f"Total: {found_overall:,} / {total_overall:,} sequences found ({overall_percentage:.2f}%)\n\n"
    )

    stats_lines = [
        "# Stats\n\n",
        "| Letter | Found    | Percentage | Letter | Found    | Percentage |\n",
        "|--------|----------|------------|--------|----------|------------|\n",
    ]

    for k in range(13):
        letter1 = letters[k]
        letter2 = letters[k + 13]
        found1, percentage1 = all_stats[letter1][1], all_stats[letter1][2]
        found2, percentage2 = all_stats[letter2][1], all_stats[letter2][2]
        row = (
            f"| {letter1.upper():<6} | {found1:<8,} | {percentage1:>9.2f}% "
            f"| {letter2.upper():<6} | {found2:<8,} | {percentage2:>9.2f}% |\n"
        )
        stats_lines.append(row)

    stats_lines.append("\n| Total Sequences Found | Percentage |\n")
    stats_lines.append("|-----------------------|------------|\n")
    stats_lines.append(f"| {found_overall:<21,} | {overall_percentage:>9.2f}% |\n")

    with open(STATS_FILE_PATH, "w") as stats_file:
        stats_file.writelines(stats_lines)
