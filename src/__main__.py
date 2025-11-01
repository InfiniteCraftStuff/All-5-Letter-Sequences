import os.path

import logging

from .stats import get_all_stats


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)

LOG_FILE_PATH = os.path.join(BASE_DIR, "logs", "console.log")
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE_PATH)],
)


def main():
    get_all_stats()


if __name__ == "__main__":
    main()
