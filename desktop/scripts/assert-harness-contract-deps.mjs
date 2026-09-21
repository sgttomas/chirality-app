#!/usr/bin/env node

import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const frontendRoot = path.resolve(__dirname, '..');
const contractSrc = path.join(frontendRoot, 'packages', 'harness-contract', 'src');
const appSrc = path.join(frontendRoot, 'src');
const rollbackTest = path.join(
  appSrc,
  '__tests__',
  'lib',
  'harness-contract-rollback.test.ts'
);
const forbiddenSpecifiers = [
  /^node:/,
  /^react($|\/)/,
  /^react-dom($|\/)/,
  /^next($|\/)/,
  /^electron($|\/)/,
  /^@anthropic-ai\//
];
const allowedFacadeSpecifiers = [/^@chirality\/runtime-contracts(?:$|\/)/];

async function listSourceFiles(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...(await listSourceFiles(fullPath)));
      continue;
    }
    if (entry.isFile() && /\.tsx?$/.test(fullPath)) {
      files.push(fullPath);
    }
  }
  return files;
}

function importSpecifiers(source) {
  const specifiers = [];
  const importExportPattern =
    /\b(?:import|export)\s+(?:type\s+)?(?:[^'"]*?\s+from\s+)?['"]([^'"]+)['"]/g;
  const dynamicImportPattern = /\bimport\s*\(\s*['"]([^'"]+)['"]\s*\)/g;
  for (const pattern of [importExportPattern, dynamicImportPattern]) {
    let match;
    while ((match = pattern.exec(source)) !== null) {
      specifiers.push(match[1]);
    }
  }
  return specifiers;
}

function resolveRelativeImport(filePath, specifier) {
  const resolved = path.resolve(path.dirname(filePath), specifier);
  return path.extname(resolved) ? resolved : `${resolved}.ts`;
}

const failures = [];
for (const filePath of await listSourceFiles(contractSrc)) {
  const source = await readFile(filePath, 'utf8');
  for (const specifier of importSpecifiers(source)) {
    if (forbiddenSpecifiers.some((pattern) => pattern.test(specifier))) {
      failures.push(`${path.relative(frontendRoot, filePath)} imports forbidden ${specifier}`);
      continue;
    }
    if (specifier.startsWith('.')) {
      const resolved = resolveRelativeImport(filePath, specifier);
      if (!resolved.startsWith(`${contractSrc}${path.sep}`)) {
        failures.push(
          `${path.relative(frontendRoot, filePath)} escapes contract package via ${specifier}`
        );
      }
      continue;
    }
    if (allowedFacadeSpecifiers.some((pattern) => pattern.test(specifier))) {
      continue;
    }
    failures.push(`${path.relative(frontendRoot, filePath)} imports external package ${specifier}`);
  }
}

let rollbackFacadeImports = 0;
for (const filePath of await listSourceFiles(appSrc)) {
  const source = await readFile(filePath, 'utf8');
  for (const specifier of importSpecifiers(source)) {
    if (!/^@chirality\/harness-contract(?:$|\/)/.test(specifier)) {
      continue;
    }
    if (filePath === rollbackTest) {
      rollbackFacadeImports += 1;
      continue;
    }
    failures.push(
      `${path.relative(frontendRoot, filePath)} retains executable facade import ${specifier}`
    );
  }
}

if (rollbackFacadeImports !== 13) {
  failures.push(
    `${path.relative(frontendRoot, rollbackTest)} must retain exactly 13 facade export probes; found ${rollbackFacadeImports}`
  );
}

const packageJson = JSON.parse(await readFile(path.join(frontendRoot, 'package.json'), 'utf8'));
if (packageJson.dependencies?.['@chirality/harness-contract'] !== undefined) {
  failures.push('package.json retains load-bearing @chirality/harness-contract dependency');
}

const packageLock = JSON.parse(await readFile(path.join(frontendRoot, 'package-lock.json'), 'utf8'));
if (packageLock.packages?.['']?.dependencies?.['@chirality/harness-contract'] !== undefined) {
  failures.push('package-lock.json root package retains load-bearing @chirality/harness-contract dependency');
}

for (const configName of ['tsconfig.json', 'next.config.mjs']) {
  const source = await readFile(path.join(frontendRoot, configName), 'utf8');
  if (source.includes('@chirality/harness-contract')) {
    failures.push(`${configName} retains load-bearing @chirality/harness-contract wiring`);
  }
}

if (failures.length > 0) {
  for (const failure of failures) {
    console.error(failure);
  }
  process.exitCode = 1;
} else {
  console.log('harness contract dependency lint passed');
}
