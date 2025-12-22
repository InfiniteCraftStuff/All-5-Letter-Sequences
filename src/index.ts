import { getAllStats } from "./stats";
import { processSingleFile } from "./processing";

function main() {
  const command = process.argv[2];

  if (command === "stats") {
    return getAllStats();
  }

  const filePath = process.argv[3];

  if (!filePath) {
    console.error("No file path provided");
    return;
  }

  if (command === "file") {
    return processSingleFile(filePath);
  }
}

main();
