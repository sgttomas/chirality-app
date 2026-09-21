import { describe, expect, it } from 'vitest';
import { sanitizeLabel } from '../../lib/harness/sanitize';

describe('sanitizeLabel', () => {
  it('keeps clean labels unchanged', () => {
    expect(sanitizeLabel('PKG 05 Filesystem Execution Model')).toBe(
      'PKG 05 Filesystem Execution Model'
    );
  });

  it('replaces illegal filesystem characters with hyphen', () => {
    expect(sanitizeLabel('UI: Login/Auth <v2>|draft')).toBe('UI- Login-Auth -v2--draft');
  });

  it('collapses internal whitespace and trims edges', () => {
    expect(sanitizeLabel('   Build    and    Package   ')).toBe('Build and Package');
  });

  it('applies sanitization steps in declared order', () => {
    expect(sanitizeLabel('  a :  b  ')).toBe('a - b');
  });

  it('returns empty string when input is whitespace-only', () => {
    expect(sanitizeLabel('    ')).toBe('');
  });
});
