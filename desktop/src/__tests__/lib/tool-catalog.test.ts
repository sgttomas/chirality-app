import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { renderHarnessToolCatalog } from '@chirality/runtime-contracts/tool-catalog';
import { listHarnessToolDescriptors } from '@chirality/runtime-contracts/tool-descriptor';

describe('harness tool catalog', () => {
  it('matches the generated descriptor registry catalog', async () => {
    const catalogPath = path.resolve(process.cwd(), 'docs', 'harness', 'tool_catalog.md');
    await expect(readFile(catalogPath, 'utf8')).resolves.toBe(renderHarnessToolCatalog());
  });

  it('enumerates every descriptor exactly once', () => {
    const catalog = renderHarnessToolCatalog();
    for (const descriptor of listHarnessToolDescriptors()) {
      expect(catalog.match(new RegExp(`^\\| ${descriptor.name} \\|`, 'gm'))).toHaveLength(1);
    }
  });
});
