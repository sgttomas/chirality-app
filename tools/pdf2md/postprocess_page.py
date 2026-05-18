#!/usr/bin/env python3
"""
postprocess_page.py
Apply 10-rule deterministic cleanup to VLM-generated markdown.

Direct Python port of the 10-rule pipeline from
edgequake-pdf2md/src/pipeline/postprocess.rs. Rules must run in
the defined order (CRLF normalization before fence stripping, etc.).

Usage:
    python3 postprocess_page.py <input.md> [<output.md>]

Inputs:
    input.md  — markdown file to clean
    output.md — optional output path (default: overwrite input in-place)

Outputs:
    Cleaned markdown file. Prints "{filename}: cleaned" to stdout.

Example:
    python3 postprocess_page.py page_0001.md
    python3 postprocess_page.py raw.md cleaned.md
"""

import re
import sys
from pathlib import Path


# ── Rule 1: Normalise line endings ──────────────────────────────────────────

def normalise_line_endings(text):
    """CRLF → LF. Must run before fence stripping so regex works on both."""
    return text.replace('\r\n', '\n').replace('\r', '\n')


# ── Rule 2: Strip outer markdown fences ─────────────────────────────────────

def strip_markdown_fences(text):
    """Remove a single layer of outer markdown code fences wrapping the output."""
    trimmed = text.strip()
    if not trimmed:
        return trimmed

    lines = trimmed.split('\n')
    if not lines:
        return trimmed

    # Strip leading fence opener: ``` or ```<lang>
    first = lines[0].strip()
    if first.startswith('```') and '`' not in first[3:]:
        lines.pop(0)

    if not lines:
        return ''

    # Strip trailing fence closer: exactly ```
    last = lines[-1].strip()
    if last == '```':
        lines.pop()

    return '\n'.join(lines)


# ── Rule 3: Trim trailing whitespace per line ───────────────────────────────

def trim_trailing_whitespace(text):
    return '\n'.join(line.rstrip() for line in text.split('\n'))


# ── Rule 4: Collapse excessive blank lines ──────────────────────────────────

_RE_BLANK_LINES = re.compile(r'\n{4,}')

def collapse_blank_lines(text):
    """Collapse 3+ consecutive blank lines down to 2."""
    return _RE_BLANK_LINES.sub('\n\n\n', text)


# ── Rule 5: Normalise heading spacing ───────────────────────────────────────

def normalise_heading_spacing(text):
    """Ensure a blank line before each heading (unless at the very start)."""
    lines = text.split('\n')
    result = []
    for i, line in enumerate(lines):
        is_heading = line.startswith('#') and (' ' in line or line.strip() in {'#', '##', '###', '####'})
        if is_heading and i > 0:
            # Ensure the preceding line is blank
            while result and result[-1] == '':
                result.pop()
            result.append('')
        result.append(line)
    return '\n'.join(result)


# ── Rule 6: Fix broken GFM tables ──────────────────────────────────────────

def _is_table_row(line):
    trimmed = line.strip()
    return trimmed.startswith('|') and trimmed.endswith('|') and len(trimmed) > 2


def _is_separator_row(line):
    trimmed = line.strip()
    if not trimmed.startswith('|'):
        return False
    return all(c in '|-: ' for c in trimmed)


def fix_broken_tables(text):
    """Insert missing separator rows after table headers."""
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if _is_table_row(line) and not _is_separator_row(line):
            result.append(line)
            # Check if next line is a data row (not a separator)
            next_line = lines[i + 1] if i + 1 < len(lines) else ''
            if _is_table_row(next_line) and not _is_separator_row(next_line):
                col_count = max(1, line.count('|') - 1)
                sep = '|' + ' --- |' * col_count
                result.append(sep)
            i += 1
            continue
        result.append(line)
        i += 1
    return '\n'.join(result)


# ── Rule 7: Remove spurious mid-table separator rows ───────────────────────

def remove_mid_table_separators(text):
    """Only allow separator at position 2 (after header row) within each table."""
    lines = text.split('\n')
    result = []
    in_table = False
    table_line_count = 0

    for line in lines:
        if _is_table_row(line):
            if not in_table:
                in_table = True
                table_line_count = 0
            table_line_count += 1

            if _is_separator_row(line) and table_line_count != 2:
                continue  # skip spurious separator
            result.append(line)
        else:
            in_table = False
            table_line_count = 0
            result.append(line)

    return '\n'.join(result)


# ── Rule 8: Remove hallucinated image links ─────────────────────────────────

_RE_IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)]*)\)')

_FAKE_DOMAINS = [
    'example.com', 'placeholder.com', 'via.placeholder.com',
    'dummyimage.com', 'lorempixel.com', 'picsum.photos', 'placehold.it',
]

_LOCAL_ASSET_PREFIXES = ('figures/', 'images/', 'tables/', './figures/', './images/', './tables/')


def _is_placeholder_url(url):
    u = url.strip()
    if not u:
        return True
    if u.startswith(_LOCAL_ASSET_PREFIXES):
        return False
    if not u.startswith('http://') and not u.startswith('https://'):
        return True
    return any(d in u for d in _FAKE_DOMAINS)


def remove_hallucinated_images(text):
    """Replace hallucinated image links with italic alt text."""
    def replacer(m):
        alt = m.group(1).strip()
        url = m.group(2)
        if _is_placeholder_url(url):
            return f'*{alt}*' if alt else ''
        return m.group(0)
    return _RE_IMAGE.sub(replacer, text)


# ── Rule 9: Strip invisible Unicode ─────────────────────────────────────────

_INVISIBLE_CHARS = str.maketrans({
    '\u200B': None,  # zero-width space
    '\uFEFF': None,  # BOM / zero-width no-break space
    '\u00AD': None,  # soft hyphen
    '\u200C': None,  # zero-width non-joiner
    '\u200D': None,  # zero-width joiner
    '\u2060': None,  # word joiner
})


def remove_invisible_chars(text):
    return text.translate(_INVISIBLE_CHARS)


# ── Rule 10: Ensure final newline ───────────────────────────────────────────

def ensure_final_newline(text):
    trimmed = text.rstrip()
    return (trimmed + '\n') if trimmed else '\n'


# ── Pipeline ────────────────────────────────────────────────────────────────

def postprocess(text):
    """Apply all 10 rules in order. Pure text → text, no I/O."""
    s = normalise_line_endings(text)      # 1
    s = strip_markdown_fences(s)          # 2
    s = trim_trailing_whitespace(s)       # 3
    s = collapse_blank_lines(s)           # 4
    s = normalise_heading_spacing(s)      # 5
    s = fix_broken_tables(s)              # 6
    s = remove_mid_table_separators(s)    # 7
    s = remove_hallucinated_images(s)     # 8
    s = remove_invisible_chars(s)         # 9
    s = ensure_final_newline(s)           # 10
    return s


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input.md> [<output.md>]", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path

    if not input_path.is_file():
        print(f"ERROR: Not a file: {input_path}", file=sys.stderr)
        sys.exit(1)

    original = input_path.read_text(encoding='utf-8')
    cleaned = postprocess(original)
    output_path.write_text(cleaned, encoding='utf-8')
    print(f"{output_path.name}: cleaned")


if __name__ == '__main__':
    main()
