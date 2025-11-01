import { basename } from "node:path";
import { getSequencesFromFile, markSequencesAsFound } from "./database";

function processBatch(sequences: string[]) {
  const groupedSequences: string[][] = Array.from({ length: 26 }, () => []);

  for (const seq of sequences) {
    const loweredSeq = seq.toLowerCase();
    const index = loweredSeq.charCodeAt(1) - 97;
    if (index < 0 || index >= 26) {
      console.error(`Invalid sequence ${loweredSeq}. Skipping.`);
      continue;
    }
    groupedSequences[index].push(loweredSeq);
  }

  for (const batch of groupedSequences) {
    if (batch.length > 0) {
      console.info(
        `Processing batch ${batch[0].slice(0, 2)} (${batch.length} sequences)`
      );
      const batchStart = Date.now();
      markSequencesAsFound(batch);
      console.info(
        `Batch ${batch[0].slice(0, 2)} processed in ${(
          (Date.now() - batchStart) /
          1000
        ).toFixed(2)} seconds`
      );
    }
  }
}

function processLetter(sequences: string[]) {
  console.info("\n--- Processing sequences ---");
  const startTime = Date.now();

  processBatch(sequences);
  console.info(
    `--- Completed in ${((Date.now() - startTime) / 1000).toFixed(
      2
    )} seconds ---\n`
  );
}

/**
 * Process a single file, splitting sequences by letter and then processing them.
 */
export async function processSingleFile(filePath: string) {
  const fileName = basename(filePath);
  console.info(`\n--- Processing single file: ${fileName} ---`);

  const sequences = await getSequencesFromFile(filePath);
  if (sequences.length === 0) {
    console.info("No sequences found. Skipping.\n");
    return;
  }

  // Split sequences by letter
  const groupedSequences: string[][] = Array.from({ length: 26 }, () => []);
  for (const seq of sequences) {
    const loweredSeq = seq.toLowerCase(); // Ensure sequence is lowercase
    const index = loweredSeq.charCodeAt(0) - 97;
    if (index >= 0 && index < 26) {
      groupedSequences[index].push(loweredSeq);
    }
  }

  // Now process each batch of sequences for each letter
  for (const batch of groupedSequences) {
    if (batch.length > 0) {
      console.info(`Processing batch (${batch.length} sequences)`);
      processLetter(batch);
    }
  }
}
