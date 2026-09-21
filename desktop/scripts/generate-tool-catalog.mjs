#!/usr/bin/env node

import path from 'node:path';
import { mkdir, writeFile } from 'node:fs/promises';
// Same resolved module as src/__tests__/lib/tool-catalog.test.ts: the test
// imports the deprecated `@chirality/harness-contract/tool-catalog` facade,
// which re-exports `@chirality/runtime-contracts/tool-catalog` (built dist).
// Importing the runtime contracts package directly lands on that identical
// dist module, so generator and drift check share one renderer.
import { renderHarnessToolCatalog } from '@chirality/runtime-contracts/tool-catalog';

const repoRelativeCatalogPath = path.join('docs', 'harness', 'tool_catalog.md');
const catalogPath = path.resolve(process.cwd(), repoRelativeCatalogPath);

// Catalog-vs-descriptor drift is owned by a single check:
// src/__tests__/lib/tool-catalog.test.ts (runs in CI through the
// release-quality wrapper's full_test evidence command). The former
// `--check` mode here duplicated that exact equality assertion and had no
// CI or package.json caller, so this script is now write-only.
async function main() {
  const rendered = renderHarnessToolCatalog();

  await mkdir(path.dirname(catalogPath), { recursive: true });
  await writeFile(catalogPath, rendered, 'utf8');
  process.stdout.write(`wrote ${repoRelativeCatalogPath}\n`);
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  process.stderr.write(`${message}\n`);
  process.exitCode = 1;
});
