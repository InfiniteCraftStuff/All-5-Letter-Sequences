import * as path from "node:path";

import { getStatistics } from "./database";

const BASE_DIR = path.dirname(import.meta.dir);
const STATS_FILE_PATH = path.join(BASE_DIR, "STATS.md");

export function getAllStats() {
  const allStats = getStatistics();

  const foundOverall = allStats.reduce((sum, s) => sum + s.found, 0);
  const totalOverall = 26 ** 5;
  const overallPercentage = (foundOverall / totalOverall) * 100;

  const statLines = [
    "# Stats\n\n",
    "| Letter | Found    | Percentage | Letter | Found    | Percentage |\n",
    "|--------|----------|------------|--------|----------|------------|\n",
  ];

  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" as const;
  for (let k = 0; k <= 12; k++) {
    const letter1 = letters[k]!;
    const letter2 = letters[k + 13]!;
    const stat1 = allStats.find((s) => s.letter.toUpperCase() === letter1)!;
    const stat2 = allStats.find((s) => s.letter.toUpperCase() === letter2)!;
    const found1 = stat1.found;
    const percentage1 = stat1.percentage;
    const found2 = stat2.found;
    const percentage2 = stat2.percentage;
    const row = `| ${letter1.padEnd(6)} | ${found1
      .toLocaleString()
      .padEnd(8)} | ${percentage1.toFixed(2).padStart(9)}% | ${letter2.padEnd(
      6
    )} | ${found2.toLocaleString().padEnd(8)} | ${percentage2
      .toFixed(2)
      .padStart(9)}% |\n`;
    statLines.push(row);
  }

  statLines.push("\n| Total Sequences Found | Percentage |\n");
  statLines.push("|-----------------------|------------|\n");
  statLines.push(
    `| ${foundOverall.toLocaleString().padEnd(21)} | ${overallPercentage
      .toFixed(2)
      .padStart(9)}% |\n`
  );

  Bun.write(STATS_FILE_PATH, statLines.join(""));
}
