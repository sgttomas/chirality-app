import { describe, expect, it } from 'vitest';
import { hasAnsiEscapeCodes, renderAnsiToHtml } from '../../lib/shell/ansi';

describe('ansi helpers', () => {
  it('detects ANSI escape sequences', () => {
    expect(hasAnsiEscapeCodes('\u001b[32mOK\u001b[0m')).toBe(true);
    expect(hasAnsiEscapeCodes('plain text')).toBe(false);
  });

  it('renders ANSI text to class-based html', () => {
    const html = renderAnsiToHtml('\u001b[31mERR\u001b[0m');
    expect(html).toContain('ansi-red-fg');
    expect(html).toContain('ERR');
  });
});
