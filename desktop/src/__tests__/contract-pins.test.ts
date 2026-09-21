import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import {
  CONTRACT_PIN_MANIFEST,
  type ContractPin,
  type ContractPinTarget
} from './contract-pins.manifest';

function describePin(pin: ContractPin): string {
  switch (pin.kind) {
    case 'contains':
      return `must contain ${JSON.stringify(pin.value)}`;
    case 'notContains':
      return `must NOT contain ${JSON.stringify(pin.value)}`;
    case 'notMatches':
      return `must NOT match /${pin.pattern}/`;
    case 'jsonPathContains':
      return `JSON ${pin.jsonPath.join('.')} must contain ${JSON.stringify(pin.value)}`;
    case 'jsonPathEquals':
      return `JSON ${pin.jsonPath.join('.')} must equal ${JSON.stringify(pin.value)}`;
  }
}

function resolveJsonPath(raw: string, jsonPath: string[], file: string): unknown {
  let current: unknown = JSON.parse(raw);
  for (const segment of jsonPath) {
    if (current === null || typeof current !== 'object') {
      throw new Error(`${file}: JSON path ${jsonPath.join('.')} is unreachable at '${segment}'`);
    }
    current = (current as Record<string, unknown>)[segment];
  }
  return current;
}

function pinHolds(raw: string, pin: ContractPin, file: string): boolean {
  switch (pin.kind) {
    case 'contains':
      return raw.includes(pin.value);
    case 'notContains':
      return !raw.includes(pin.value);
    case 'notMatches':
      return !new RegExp(pin.pattern).test(raw);
    case 'jsonPathContains': {
      const resolved = resolveJsonPath(raw, pin.jsonPath, file);
      if (typeof resolved === 'string') {
        return resolved.includes(pin.value);
      }
      if (Array.isArray(resolved)) {
        return resolved.includes(pin.value);
      }
      return false;
    }
    case 'jsonPathEquals':
      return resolveJsonPath(raw, pin.jsonPath, file) === pin.value;
  }
}

describe('contract pins', () => {
  it.for(CONTRACT_PIN_MANIFEST)(
    '$file holds every pinned invariant',
    async (target: ContractPinTarget, { skip }) => {
      const absolutePath = path.resolve(process.cwd(), target.file);
      if (target.allowMissing && !existsSync(absolutePath)) {
        console.warn(
          `contract-pins: skipped ${target.file} (file not present at ${absolutePath})`
        );
        skip();
        return;
      }

      const raw = await readFile(absolutePath, 'utf8');
      const failures = target.pins
        .filter((pin) => !pinHolds(raw, pin, target.file))
        .map((pin) => `${target.file}: ${describePin(pin)}`);

      expect(failures, `Broken contract pins in ${target.file}`).toEqual([]);
    }
  );
});
