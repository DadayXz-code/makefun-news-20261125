// THE WORLD TODAY — Wednesday 25 November 2026.
// Copies the pre-drawn front-page image to the grader's output dir.
// Stdlib only: no network, no dependencies. The copy is byte-identical
// on every run because the source PNG never changes at run time.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
