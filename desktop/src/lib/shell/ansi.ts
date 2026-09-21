import { AnsiUp } from 'ansi_up';

const ANSI_PATTERN = /\u001b\[[0-9;]*m/;

const ANSI_CONVERTER = new AnsiUp();
ANSI_CONVERTER.use_classes = true;

export function hasAnsiEscapeCodes(value: string): boolean {
  return ANSI_PATTERN.test(value);
}

export function renderAnsiToHtml(value: string): string {
  return ANSI_CONVERTER.ansi_to_html(value);
}
