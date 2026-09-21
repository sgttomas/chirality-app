import { HarnessError } from '@chirality/runtime-contracts/errors';

const ILLEGAL_LABEL_CHARACTERS = /[\/\\:*?"<>|]/g;
const CONSECUTIVE_WHITESPACE = /\s+/g;

/**
 * Implements SPEC Section 10.1:
 * 1. Replace illegal filesystem characters with '-'
 * 2. Collapse consecutive whitespace to one space
 * 3. Trim leading/trailing whitespace
 */
export function sanitizeLabel(name: string): string {
  return name.replace(ILLEGAL_LABEL_CHARACTERS, '-').replace(CONSECUTIVE_WHITESPACE, ' ').trim();
}

export function sanitizeNonEmptyLabel(name: string, field: string): string {
  const sanitized = sanitizeLabel(name);
  if (!sanitized) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      `${field} resolves to an empty label after sanitization`,
      { field, value: name }
    );
  }

  return sanitized;
}
