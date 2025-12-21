import { getAllStats } from "./stats";

function main() {
  if (process.argv[2] === "stats") {
    return getAllStats();
  }
}

main();
