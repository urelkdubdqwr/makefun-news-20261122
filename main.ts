import { mkdirSync, copyFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));

function stageEntry(outputDir: string): void {
  const src = join(scriptDir, "entry.png");
  const dst = join(outputDir, "entry.png");

  if (!existsSync(src)) {
    console.warn(`Warning: entry.png not found at ${src}; nothing to stage.`);
    return;
  }

  mkdirSync(outputDir, { recursive: true });
  copyFileSync(src, dst);
  console.log(`staged entry.png from ${src} to ${dst}`);
}

const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
stageEntry(outputDir);
