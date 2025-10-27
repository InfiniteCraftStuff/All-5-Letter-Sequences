import { Database } from "bun:sqlite";

async function main() {
  const letters = "abcdefghijklmnopqrstuvwxyz" as const;
  const dbDir = "./databases/sequences" as const;
  const outputDbPath = "databases/database.db" as const;

  const outputDb = new Database(outputDbPath);

  outputDb.run(`
    CREATE TABLE sequences (
      sequence TEXT PRIMARY KEY,
      found BOOLEAN
    )
  `);

  let totalRows = 0;

  for (const firstLetter of letters) {
    const dbPath = `${dbDir}/${firstLetter}.db` as const;

    const inputDb = new Database(dbPath);
    console.log(`Processing ${dbPath}...`);

    for (const secondLetter of letters) {
      const tableName = `"${firstLetter}${secondLetter}"` as const;

      const rows = inputDb.prepare(`SELECT sequence, found FROM ${tableName}`).all() as { sequence: string; found: number }[];

      const values = rows.map(row => `('${row.sequence}', ${row.found})`).join(', ');
      const sql = `INSERT INTO sequences (sequence, found) VALUES ${values}` as const;

      outputDb.run(sql);

      totalRows += rows.length;
      console.log(`  Copied ${rows.length} rows from ${tableName}`); 
    }

    inputDb.close();
  }

  outputDb.run("CREATE INDEX IF NOT EXISTS idx_seq ON sequences(sequence)");
  outputDb.run("VACUUM");
  outputDb.close();

  console.log(`\nMigration complete! Total rows: ${totalRows}`);
  console.log(`Combined DB size: ${(Bun.file(outputDbPath).size / (1024 * 1024)).toFixed(1)} MB`);
  console.log(`Verify: bunx sqlite3 ${outputDbPath} "SELECT COUNT(*) FROM sequences;"`);
}

await main();
