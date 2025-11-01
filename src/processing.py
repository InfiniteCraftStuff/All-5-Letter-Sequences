import os
from time import time
import logging

from .database import update_sequences, get_sequences_from_file


def process_batch(sequences: list[str]):
    grouped_sequences: list[list[str]] = [[] for _ in range(26)]

    for seq in sequences:
        seq = seq.lower()
        index = ord(seq[1]) - 97
        if index < 0 or index >= 26:
            logging.error(f"Invalid sequence {seq}. Skipping.")
            continue
        grouped_sequences[ord(seq[1]) - 97].append(seq)

    for batch in grouped_sequences:
        if batch:
            logging.info(f"Processing batch {batch[0][:2]} ({len(batch)} sequences)")
            batch_start = time()
            update_sequences(batch)
            logging.info(f"Batch {batch[0][:2]} processed in {time() - batch_start:.2f} seconds")


def process_letter(sequences: list[str]):
    logging.info("\n--- Processing sequences ---")
    start_time = time()

    process_batch(sequences)
    logging.info(f"--- Completed in {time() - start_time:.2f} seconds ---\n")


def process_single_file(file_path: str):
    """Process a single file, splitting sequences by letter and then processing them."""
    file_name = os.path.basename(file_path)
    logging.info(f"\n--- Processing single file: {file_name} ---")

    sequences = get_sequences_from_file(file_path)
    if not sequences:
        logging.info("No sequences found. Skipping.\n")
        return

    grouped_sequences: list[list[str]] = [[] for _ in range(26)]
    for seq in sequences:
        seq = seq.lower()
        grouped_sequences[ord(seq[0]) - 97].append(seq)

    for batch in grouped_sequences:
        if batch:
            logging.info(f"Processing batch ({len(batch)} sequences)")
            process_letter(batch)
