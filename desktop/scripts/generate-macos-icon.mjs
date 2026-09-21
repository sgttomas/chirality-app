#!/usr/bin/env node
/**
 * generate-macos-icon.mjs — ONE-TIME icon generator. NOT PART OF THE BUILD GRAPH.
 *
 * Nothing in `package.json` `scripts` invokes this file, and `npm run build`,
 * `build:electron`, `desktop:pack` and `desktop:dist` never call it. It exists
 * so the committed `build/icon.icns` is reproducible from the committed
 * `build/icon-macos.svg`. Regenerate manually, by hand, only when the icns-tuned
 * artwork changes:
 *
 *     node ./scripts/generate-macos-icon.mjs
 *     node ./scripts/generate-macos-icon.mjs --keep-iconset --png-dir /tmp/icon-proof
 *
 * DEPENDENCY CAVEAT (deliberate, do not "fix" by adding a dependency):
 * this script requires `sharp` at runtime, which is present in
 * `frontend/node_modules` only TRANSITIVELY (next@15.5 -> sharp, pinned to
 * 0.35.3 by the `overrides` block). `sharp` is intentionally NOT added to
 * `dependencies`/`devDependencies`: the icns is a committed binary artifact, so
 * the build never needs a rasterizer, and adding one would expand the packaged
 * dependency boundary for no runtime benefit. If a future `next` drops the
 * transitive `sharp`, this script stops working while the build keeps working;
 * regenerate with any offline vector rasterizer instead and keep the geometry
 * from `build/icon-macos.svg`.
 *
 * Offline by construction: reads a local SVG, rasterizes in-process through
 * sharp/libvips/librsvg, and shells out only to Apple's own `/usr/bin/iconutil`.
 * No network access, no downloaded toolchain (electron-builder's own
 * SVG->icns path fetches a toolset from GitHub, which the project's offline
 * packaging posture forbids — committing the icns bypasses that entirely).
 */

import { execFileSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const frontendRoot = path.resolve(scriptDirectory, '..');
const sourceSvg = path.join(frontendRoot, 'build', 'icon-macos.svg');
const outputIcns = path.join(frontendRoot, 'build', 'icon.icns');

/** The ten representations `iconutil` requires for a complete macOS iconset. */
const REPRESENTATIONS = [
  ['icon_16x16.png', 16],
  ['icon_16x16@2x.png', 32],
  ['icon_32x32.png', 32],
  ['icon_32x32@2x.png', 64],
  ['icon_128x128.png', 128],
  ['icon_128x128@2x.png', 256],
  ['icon_256x256.png', 256],
  ['icon_256x256@2x.png', 512],
  ['icon_512x512.png', 512],
  ['icon_512x512@2x.png', 1024]
];

const args = process.argv.slice(2);
const keepIconset = args.includes('--keep-iconset');
const pngDirectoryIndex = args.indexOf('--png-dir');
const pngDirectory =
  pngDirectoryIndex === -1 ? null : path.resolve(args[pngDirectoryIndex + 1] ?? '.');

const { default: sharp } = await import('sharp');
const svg = await readFile(sourceSvg);

/**
 * Render the vector natively at the target size (density scales librsvg's
 * vector rasterization, so small representations stay crisp instead of being
 * box-filtered down from 1024), then pin exact pixel dimensions.
 */
async function render(size) {
  return sharp(svg, { density: Math.max(1, Math.round((72 * size) / 1024)) })
    .resize(size, size, {
      fit: 'contain',
      background: { r: 0, g: 0, b: 0, alpha: 0 }
    })
    .png({ compressionLevel: 9 })
    .toBuffer();
}

const iconsetDirectory = keepIconset
  ? path.join(frontendRoot, 'build', 'icon.iconset')
  : path.join(mkdtempSync(path.join(os.tmpdir(), 'chirality-icns-')), 'icon.iconset');
mkdirSync(iconsetDirectory, { recursive: true });
if (pngDirectory) {
  mkdirSync(pngDirectory, { recursive: true });
}

for (const [name, size] of REPRESENTATIONS) {
  const png = await render(size);
  writeFileSync(path.join(iconsetDirectory, name), png);
  if (pngDirectory) {
    writeFileSync(path.join(pngDirectory, `proof-${size}.png`), png);
  }
  process.stdout.write(`rendered ${name} (${size}x${size}, ${png.length} bytes)\n`);
}

execFileSync('/usr/bin/iconutil', ['-c', 'icns', iconsetDirectory, '-o', outputIcns], {
  stdio: 'inherit'
});
process.stdout.write(`wrote ${outputIcns}\n`);

if (!keepIconset) {
  rmSync(path.dirname(iconsetDirectory), { recursive: true, force: true });
}
