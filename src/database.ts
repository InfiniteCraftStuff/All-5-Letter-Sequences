import { Database } from "bun:sqlite";
import * as path from "node:path";

const BASE_DIR = path.dirname(import.meta.dir);
const DB_FILE = path.join(BASE_DIR, "database", "database.db");

function connectDb() {
  return new Database(DB_FILE);
}

export function getIsFound(sequence: string): boolean {
  const loweredSequence = sequence.toLowerCase();
  if (loweredSequence.length !== 5) {
    throw new Error("Sequence must be 5 letters");
  }

  const db = connectDb();
  const query = "SELECT found FROM sequences WHERE sequence = ?";
  const result = db.query<{ found: 0 | 1 }, string>(query).get(loweredSequence);
  db.close();
  return !!result?.found;
}

export function markSequencesAsFound(sequences: string[]): void {
  if (!sequences.length) {
    return;
  }

  const db = connectDb();
  const loweredSequences = sequences.map((seq) => seq.toLowerCase());
  const placeholders = loweredSequences.map(() => "?").join(",");
  const query = `UPDATE sequences SET found = 1 WHERE sequence IN (${placeholders})`;
  const params = [...loweredSequences];
  db.prepare(query).run(...params);
  db.close();
}

export async function getSequencesFromFile(
  filePath: string
): Promise<string[]> {
  try {
    const content = await Bun.file(filePath).text();
    return content
      .split("\n")
      .map((line) => line.trim().toLowerCase())
      .filter((line) => line.length > 0);
  } catch (error) {
    if (error instanceof Error && "code" in error && error.code === "ENOENT") {
      console.warn(`File not found: ${filePath}`);
    } else {
      console.error(`Error reading file ${filePath}:`, error);
    }
    return [];
  }
}

export function getNotFoundSequences(): string[] {
  const db = connectDb();
  const query = "SELECT sequence FROM sequences WHERE found = 0";
  const results = db.query<{ sequence: string }, []>(query).all();
  db.close();
  return results.map((row) => row.sequence);
}

export function getStatistics() {
  const db = connectDb();

  const query = `
    SELECT 
      SUBSTR(sequence, 1, 1) AS letter,
      SUM(found) AS found
    FROM sequences 
    GROUP BY letter
  `;
  const results = db.query<{ letter: string; found: number }, []>(query).all();
  db.close();
  const perLetterTotal = 26 ** 4;
  return results.map((letterStat) => ({
    letter: letterStat.letter,
    found: letterStat.found,
    percentage: (letterStat.found / perLetterTotal) * 100,
  }));
}
